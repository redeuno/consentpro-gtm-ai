"""Identidade do template e leitura completa do inventário, sem rede própria."""

import hashlib
import json
import re
import urllib.parse

OWNER = "finsweet"
HOST = "github.com"
REPOSITORY = "gtm-template-consent-pro"
VERSION = "8a551897e5bfdecf03de59fa00058be442b7ac29"
GALLERY_TEMPLATE_ID = "WRGND"
NAME = "Consent Pro - GTM Template"
# Medido em 2026-10-01 na versão fixada e no .tpl oficial anterior. Só a ajuda difere nos parâmetros.
CONTENT_HASH = "775bb1ebc2f88242cc7fab3f7a4833175bd9b0f84582a1af4e3e4bb78773f8a7"
SOURCE_URL = "https://raw.githubusercontent.com/%s/%s/%s/template.tpl" % (OWNER, REPOSITORY, VERSION)


def list_all(read, path, key):
    items, seen = [], set()
    while True:
        page = read(path)
        if not isinstance(page, dict) or "error" in page or not isinstance(page.get(key, []), list):
            raise SystemExit("Invalid inventory response for " + key)
        batch = page.get(key, [])
        if any(not isinstance(item, dict) for item in batch):
            raise SystemExit("Invalid inventory item for " + key)
        items.extend(batch)
        token = page.get("nextPageToken")
        if not token:
            return items
        if not isinstance(token, str) or token in seen:
            raise SystemExit("Invalid or repeated page token for " + key)
        seen.add(token)
        path = path.split("?", 1)[0] + "?" + urllib.parse.urlencode({"pageToken": token})


def sections(data):
    if not isinstance(data, str):
        raise ValueError("templateData missing")
    parts = re.split(r"(?m)^___([A-Z_]+)___\s*$", data.replace("\r\n", "\n"))
    result = {}
    for index in range(1, len(parts), 2):
        if parts[index] in result:
            raise ValueError("duplicate template section")
        result[parts[index]] = parts[index + 1].strip()
    return result


def content_hash(data):
    parsed = sections(data)

    def without_help(value):
        if isinstance(value, dict):
            return {key: without_help(item) for key, item in value.items() if key != "help"}
        if isinstance(value, list):
            return [without_help(item) for item in value]
        return value

    payload = [without_help(json.loads(parsed["TEMPLATE_PARAMETERS"])),
               parsed["SANDBOXED_JS_FOR_WEB_TEMPLATE"], json.loads(parsed["WEB_PERMISSIONS"])]
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def inspect(template):
    data = template.get("templateData")
    try:
        info = json.loads(sections(data).get("INFO", "{}"))
        if not isinstance(info, dict):
            info = {}
    except (ValueError, TypeError):
        info = {}
    gallery = template.get("galleryReference")
    # A galeria reescreve a marca do INFO. Importação manual mantém a marca do arquivo público.
    expected_brand = "github.com_finsweet" if gallery is not None else "finsweet_consent_pro"
    name = str(template.get("name", ""))
    brand = info.get("brand") if isinstance(info.get("brand"), dict) else {}
    candidate = ("consent pro" in name.lower() or "consent pro" in str(info.get("displayName", "")).lower()
                 or brand.get("id") == "finsweet_consent_pro"
                 or isinstance(gallery, dict) and gallery.get("repository") == REPOSITORY)
    if not candidate:
        return None
    result = {"status": "blocked", "source": "gallery" if gallery is not None else "manual",
              "version": gallery.get("version") if isinstance(gallery, dict) else None,
              "templateId": template.get("templateId"), "detail": ""}
    reason = None
    if not str(template.get("templateId", "")).isdigit():
        reason = "Template id missing or invalid"
    elif (info.get("type") != "TAG" or info.get("displayName") != NAME
          or brand.get("id") != expected_brand or info.get("containerContexts") != ["WEB"]):
        reason = "Consent Pro INFO identity does not match the reviewed template"
    else:
        try:
            if content_hash(data) != CONTENT_HASH:
                reason = "Consent Pro code, parameters or permissions differ from the reviewed template"
        except (ValueError, KeyError, TypeError):
            reason = "Consent Pro template content is incomplete or invalid"
    if reason is None and gallery is not None:
        if not isinstance(gallery, dict) or gallery.get("owner") != OWNER or gallery.get("repository") != REPOSITORY:
            reason = "Gallery owner or repository does not match"
        elif gallery.get("host") != HOST:
            reason = "Gallery host does not match"
        elif gallery.get("isModified", False) is not False:
            reason = "Gallery template is modified or its modification state is invalid"
        elif gallery.get("version") != VERSION:
            reason = "Gallery version is not the reviewed pinned release"
        elif (gallery.get("galleryTemplateId") != GALLERY_TEMPLATE_ID
              or info.get("id") != "cvt_" + GALLERY_TEMPLATE_ID):
            reason = "Gallery public template id does not match the reviewed identity"
    result["status"] = "blocked" if reason else "verified"
    result["detail"] = reason or ("Gallery identity and pinned content verified" if gallery is not None
                                  else "Manual template content matches reviewed release; origin and version unverified; preserved")
    return result


def tag_type(template, container_id):
    if template is None:
        return None
    identity = inspect(template)
    if not identity or identity["status"] != "verified":
        raise SystemExit("Cannot derive a tag type from an unverified template")
    if identity["source"] == "gallery":
        return "cvt_" + GALLERY_TEMPLATE_ID
    return "cvt_%s_%s" % (container_id, template["templateId"])


def select(templates):
    candidates = [(template, inspect(template)) for template in templates]
    candidates = [(template, identity) for template, identity in candidates if identity is not None]
    if not candidates:
        return None, {"status": "missing", "source": None, "version": None,
                      "templateId": None, "detail": "No Consent Pro template found"}
    if len(candidates) != 1:
        return None, {"status": "blocked", "source": None, "version": None,
                      "templateId": None, "detail": "Multiple Consent Pro candidates; resolve ambiguity before changing anything"}
    template, identity = candidates[0]
    return (template if identity["status"] == "verified" else None), identity


def require_valid(templates):
    template, identity = select(templates)
    if identity["status"] == "blocked":
        raise SystemExit(identity["detail"])
    return template, identity


def import_path(base):
    return base + "/templates:import_from_gallery?" + urllib.parse.urlencode({
        "galleryOwner": OWNER, "galleryRepository": REPOSITORY, "gallerySha": VERSION,
        "acknowledgePermissions": "true"})


def describe(identity):
    return "%s; source=%s; version=%s; templateId=%s; %s" % (
        identity["status"], identity["source"] or "none", identity["version"] or "unverified",
        identity["templateId"] or "none", identity["detail"])
