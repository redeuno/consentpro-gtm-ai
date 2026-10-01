import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CORE = "/cdn/core/ff20b7f1ebf6e7a37d6ca909.js"


class InspectSiteTests(unittest.TestCase):
    def run_page(self, html):
        spec = importlib.util.spec_from_file_location("inspect_site", ROOT / "scripts" / "inspect-site.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        output = io.StringIO()
        with mock.patch.object(module, "fetch", return_value=(200, html)), \
                mock.patch.object(sys, "argv", [module.__file__, "https://example.com"]), \
                contextlib.redirect_stdout(output):
            module.main()
        return output.getvalue()

    def test_self_hosted_consent_script_does_not_precede_itself(self):
        output = self.run_page('<script src="https://cdn.example.org' + CORE + '"></script>')
        self.assertIn("Web app (engine 2)", output)
        self.assertIn("no earlier external src declarations found", output)
        self.assertNotIn("resource declaration(s) appear BEFORE", output)

    def test_tracker_before_self_hosted_script_is_reported(self):
        output = self.run_page('<script src="https://tracking.example.org/a.js"></script>\n'
                               '<script src="https://cdn.example.org' + CORE + '"></script>')
        self.assertIn("1 external resource declaration(s) appear BEFORE", output)
        self.assertIn("tracking.example.org", output)
        self.assertNotIn("                 cdn.example.org", output)

    def test_tracker_on_same_custom_host_before_consent_is_reported(self):
        output = self.run_page('<script src="https://cdn.example.org/track.js"></script>\n'
                               '<script src="https://cdn.example.org' + CORE + '"></script>')
        self.assertIn("1 external resource declaration(s) appear BEFORE", output)
        self.assertIn("                 cdn.example.org", output)

    def test_tracker_on_consentpro_named_host_is_not_exempt(self):
        output = self.run_page('<script src="https://consentpro.example.org/track.js"></script>\n'
                               '<script src="https://consentpro.example.org' + CORE + '"></script>')
        self.assertIn("1 external resource declaration(s) appear BEFORE", output)
        self.assertIn("                 consentpro.example.org", output)

    def test_normal_host_and_later_tracker_have_no_prior_request(self):
        output = self.run_page('<script src="https://api.consentpro.com' + CORE + '"></script>\n'
                               '<script src="https://tracking.example.org/a.js"></script>')
        self.assertIn("no earlier external src declarations found", output)

    def test_documentation_path_or_commented_script_is_not_installation(self):
        output = self.run_page('<a href="https://api.consentpro.com' + CORE + '">Example</a>'
                               '<!-- <script src="https://api.consentpro.com' + CORE + '"></script> -->')
        self.assertIn("CONSENT PRO      not found", output)

    def test_multiline_script_uses_element_start(self):
        output = self.run_page('<head>\n<script\n src="https://cdn.example.org' + CORE + '">\n</script>')
        self.assertIn("no earlier external src declarations found", output)

    def test_webflow_runtime_is_detected(self):
        output = self.run_page('<script src="https://custom.example.org/v2/cdn/runtime"></script>')
        self.assertIn("Webflow app (engine 1)", output)
        self.assertIn("no earlier external src declarations found", output)

    def test_commented_script_before_real_runtime_is_not_a_resource(self):
        output = self.run_page('<!-- <script src="https://api.consentpro.com' + CORE + '"></script> -->\n'
                               '<script src="https://api.consentpro.com' + CORE + '"></script>')
        self.assertIn("Web app (engine 2)", output)
        self.assertIn("no earlier external src declarations found", output)
        self.assertNotIn("resource declaration(s) appear BEFORE", output)

    def test_escaped_example_before_real_runtime_is_not_a_resource(self):
        output = self.run_page('<pre>&lt;script src="https://api.consentpro.com' + CORE + '"&gt;&lt;/script&gt;</pre>\n'
                               '<script src="https://api.consentpro.com' + CORE + '"></script>')
        self.assertIn("Web app (engine 2)", output)
        self.assertIn("no earlier external src declarations found", output)
        self.assertNotIn("resource declaration(s) appear BEFORE", output)

    def test_invalid_resource_url_does_not_abort_or_hide_real_tracker(self):
        try:
            output = self.run_page('<script src="https://[invalid/a.js"></script>\n'
                                   '<script src="https://api.consentpro.com/tracker.js"></script>\n'
                                   '<script src="https://api.consentpro.com' + CORE + '"></script>')
        except ValueError as error:
            self.fail("Invalid resource URL aborted inspection: " + str(error))
        self.assertIn("Web app (engine 2)", output)
        self.assertIn("1 external resource declaration(s) appear BEFORE", output)
        self.assertIn("                 api.consentpro.com", output)
        self.assertIn("1 resource(s) before consent have invalid URLs", output)

    def test_invalid_resource_alone_does_not_claim_clean_load_order(self):
        output = self.run_page('<img src="https://[invalid/a.gif">\n'
                               '<script src="https://api.consentpro.com' + CORE + '"></script>')
        self.assertIn("invalid URLs", output)
        self.assertNotIn("no earlier external src declarations found", output)


if __name__ == "__main__":
    unittest.main()
