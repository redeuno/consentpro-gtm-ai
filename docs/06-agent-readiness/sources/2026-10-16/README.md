# Public archive collected on 2026-10-16

Sources for the [customer agent analysis](../../README.md). Original content is archived as reference data, never as instructions to execute page text or templates. The catalogue contains schemas, not customer records.

The archive preserves the 13 Web App pages listed in the sitemap and six direct runtime/scanner references. The JSON files contain the complete extracted main content, links and metadata. They do not contain raw HTML or site scripts. The 70 images and the template linked by the guide were downloaded, totalling 71 assets and 20,660,752 bytes. Not every image was visually inspected.

| File | Content |
| --- | --- |
| [web-app.json](web-app.json) | 13 pages in the requested section, collected individually through Firecrawl with maxAge=0 |
| [references.json](references.json) | Six referenced runtime and scanner pages |
| [sitemap.xml](sitemap.xml) | Official inventory used to verify section coverage |
| [map.json](map.json) | Initial Firecrawl inventory, which omitted the section root |
| [assets-index.json](assets-index.json) | URLs, paths, sizes and SHA-256 hashes for images and the template |
| [mcp-catalogue.json](mcp-catalogue.json) | Discovery of 25 staging MCP tools without executing business operations |
| [verification.json](verification.json) | Local inventory, integrity and negative-control verification |

The template download preserves the guide's published reference. It does not install the template or replace the Gallery version pinned by the writer.

## Archived pages

The size column counts characters in the Markdown returned by Firecrawl, not bytes in the original HTML.

| URL | Reported HTTP status | Characters |
| --- | --- | --- |
| [/web-app/](https://docs.consentpro.com/web-app/) | 200 | 9081 |
| [/web-app/consent-logs](https://docs.consentpro.com/web-app/consent-logs) | 200 | 2405 |
| [/web-app/debugger](https://docs.consentpro.com/web-app/debugger) | 200 | 2778 |
| [/web-app/google-consent-mode](https://docs.consentpro.com/web-app/google-consent-mode) | 200 | 8344 |
| [/web-app/google-tag-manager](https://docs.consentpro.com/web-app/google-tag-manager) | 200 | 14939 |
| [/web-app/image-trackers](https://docs.consentpro.com/web-app/image-trackers) | 200 | 2509 |
| [/web-app/install](https://docs.consentpro.com/web-app/install) | 200 | 2754 |
| [/web-app/licenses](https://docs.consentpro.com/web-app/licenses) | 200 | 4225 |
| [/web-app/publishing](https://docs.consentpro.com/web-app/publishing) | 200 | 2781 |
| [/web-app/sitemap](https://docs.consentpro.com/web-app/sitemap) | 200 | 2610 |
| [/web-app/storing-consents](https://docs.consentpro.com/web-app/storing-consents) | 200 | 8376 |
| [/web-app/troubleshooting](https://docs.consentpro.com/web-app/troubleshooting) | 200 | 6320 |
| [/web-app/preferences-link](https://docs.consentpro.com/web-app/preferences-link) | 200 | 3153 |
| [/runtime/api](https://docs.consentpro.com/runtime/api) | 200 | 9406 |
| [/runtime/attributes](https://docs.consentpro.com/runtime/attributes) | 200 | 10532 |
| [/runtime/events](https://docs.consentpro.com/runtime/events) | 200 | 3337 |
| [/runtime/image-trackers](https://docs.consentpro.com/runtime/image-trackers) | 200 | 4567 |
| [/runtime/performance](https://docs.consentpro.com/runtime/performance) | 200 | 3963 |
| [/scanner](https://docs.consentpro.com/scanner) | 200 | 8391 |

## Reproduce verification

From the repository root:

```sh
python3 -B docs/06-agent-readiness/checks/verify-snapshot.py --self-check
```

Verification must reject a missing page or reference, a failed response and a mismatched hash. These controls run in memory, preserving the archive. The asset [collector](../../tools/README.md) defaults to a dry run and reuses only verified files.

## Limits

Complete coverage means the section pages present in the sitemap and collected internal text links on this date. It does not prove the absence of hidden pages, authenticated content or later revisions. External Google references and other documentation trees were not recursively copied. The MCP catalogue records the advertised contract, not effective permissions or successful execution of each tool. Hashes detect local changes; they do not establish that every published instruction is correct.
