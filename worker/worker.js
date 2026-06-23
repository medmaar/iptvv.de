/**
 * IPTV Deutschland — Kostenlos Testen Worker
 * Sprache: Deutsch · Panel: Germany
 */

const API_BASE    = "https://activationpanel.ru/api/api.php";
const API_KEY     = "35cf68cc83a3a82e1a0ac5361c7b6105";
const HOST        = "http://terry.thecontentnest.com";
const RESEND_KEY  = "re_g48VYx5C_KB6q5E9ivN21nrWkXEoxmCZf";
const FROM_EMAIL  = "IPTV Deutschland <kontakt@iptvv.de>";
const ADMIN_EMAIL = "kontakt@iptvv.de";
const SITE_URL    = "https://iptvv.de";
const PACK_NAME   = "Germany";
const WA_NUMBER   = "17828026280";
const DARK        = "#0f0c29";
const ACCENT      = "#667eea";

function jsonRes(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
  });
}

async function apiGet(params) {
  const qs = new URLSearchParams({ ...params, api_key: API_KEY });
  const res = await fetch(`${API_BASE}?${qs}`);
  return { status: res.status, text: await res.text() };
}

async function sendEmail(to, subject, html) {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${RESEND_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({ from: FROM_EMAIL, to, subject, html }),
  });
  if (!res.ok) throw new Error(`Resend (${res.status}): ${await res.text()}`);
}

function emailWrap(content) {
  return `<!DOCTYPE html>
<html lang="de">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background-color:#f2f2f2;font-family:Arial,sans-serif;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f2f2f2;padding:32px 16px;">
  <tr><td align="center">
    <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0"
           style="max-width:600px;background:#ffffff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
      <tr><td style="background:linear-gradient(135deg,#0f0c29 0%,#302b63 50%,#24243e 100%);padding:32px 40px;text-align:center;border-bottom:3px solid ${ACCENT};">
        <h1 style="margin:0;font-family:Arial,sans-serif;font-size:26px;font-weight:bold;color:#ffffff;">IPTV Deutschland</h1>
        <p style="margin:6px 0 0;font-family:Arial,sans-serif;font-size:13px;color:rgba(255,255,255,0.70);">Premium IPTV Deutschland · 4K Streaming</p>
      </td></tr>
      <tr><td style="padding:36px 40px;">${content}</td></tr>
      <tr><td style="background-color:#f8f8f8;border-top:1px solid #eeeeee;padding:18px 40px;text-align:center;">
        <p style="margin:0;font-family:Arial,sans-serif;font-size:11px;color:#aaaaaa;">
          © 2026 IPTV Deutschland · <a href="${SITE_URL}" style="color:${ACCENT};text-decoration:none;">iptvv.de</a>
        </p>
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>`;
}

function credBox(username, password, m3uUrl) {
  const server = (() => { try { return new URL(m3uUrl).origin; } catch { return HOST; } })();
  return `
  <p style="margin:0 0 8px;font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:#333333;">Xtream Codes</p>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
         style="background-color:#f8f8f8;border:1px solid #e0e0e0;border-radius:6px;margin-bottom:18px;">
    <tr><td style="padding:18px 22px;">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr><td style="padding:0 0 11px;border-bottom:1px solid #e8e8e8;">
          <p style="margin:0 0 2px;font-family:Arial,sans-serif;font-size:11px;color:#888888;text-transform:uppercase;">Server</p>
          <p style="margin:0;font-family:Arial,sans-serif;font-size:13px;color:#333333;font-weight:bold;">${server}</p>
        </td></tr>
        <tr><td style="padding:11px 0;border-bottom:1px solid #e8e8e8;">
          <p style="margin:0 0 2px;font-family:Arial,sans-serif;font-size:11px;color:#888888;text-transform:uppercase;">Benutzername</p>
          <p style="margin:0;font-family:Arial,sans-serif;font-size:13px;color:#333333;font-weight:bold;">${username}</p>
        </td></tr>
        <tr><td style="padding:11px 0 0;">
          <p style="margin:0 0 2px;font-family:Arial,sans-serif;font-size:11px;color:#888888;text-transform:uppercase;">Passwort</p>
          <p style="margin:0;font-family:Arial,sans-serif;font-size:13px;color:#333333;font-weight:bold;">${password}</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
  <p style="margin:0 0 8px;font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:#333333;">M3U-Link</p>
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
         style="background-color:#f8f8f8;border:1px solid #e0e0e0;border-radius:6px;margin-bottom:28px;">
    <tr><td style="padding:14px 20px;">
      <p style="margin:0;font-family:Arial,sans-serif;font-size:12px;color:${ACCENT};word-break:break-all;">${m3uUrl}</p>
    </td></tr>
  </table>`;
}

function ctaButton(text, url) {
  return `
  <table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:28px;">
    <tr><td style="background:linear-gradient(135deg,#667eea,#764ba2);border-radius:8px;padding:14px 32px;text-align:center;">
      <a href="${url}" style="font-family:Arial,sans-serif;font-size:15px;font-weight:bold;color:#ffffff;text-decoration:none;">${text}</a>
    </td></tr>
  </table>`;
}

function replyJaBox() {
  return `
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"
         style="background-color:#f0f0ff;border-left:4px solid ${ACCENT};border-radius:6px;margin-bottom:22px;">
    <tr><td style="padding:20px 24px;">
      <p style="margin:0 0 6px;font-family:Arial,sans-serif;font-size:14px;line-height:1.6;color:#302b63;font-weight:bold;">
        📩 Der schnellste Weg?
      </p>
      <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;line-height:1.6;color:#555555;">
        Antworten Sie einfach mit <strong>„JA"</strong> auf diese E-Mail — wir aktivieren Ihren Zugang in wenigen Minuten, kein Formular, kein Aufwand.
      </p>
    </td></tr>
  </table>`;
}

function welcomeEmail(name, username, password, m3uUrl) {
  const vorname = name && name !== "Nicht angegeben" ? name.split(" ")[0] : "";
  const greeting = vorname ? `Hallo ${vorname},` : "Hallo,";
  return emailWrap(`
    <p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:15px;color:#333333;">${greeting}</p>
    <p style="margin:0 0 16px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Ihr kostenloser Testzugang ist bereit! 🎉
    </p>
    <p style="margin:0 0 16px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Wir haben alle Länder und Sprachen freigeschaltet, damit Sie unseren Service vollständig testen können.
    </p>
    <p style="margin:0 0 24px;font-family:Arial,sans-serif;font-size:13px;line-height:1.65;color:#777777;font-style:italic;">
      Hinweis: Machen Sie sich keine Sorgen, wenn die Liste zu lang erscheint – Sie können uns jederzeit bitten, Regionen oder Kategorien auszublenden, die Sie nicht benötigen!
    </p>
    <p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:14px;color:#555555;">Hier sind Ihre Zugangsdaten:</p>
    ${credBox(username, password, m3uUrl)}
    <p style="margin:0 0 20px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Benötigen Sie Hilfe bei der Einrichtung? Antworten Sie auf diese E-Mail oder schreiben Sie uns auf WhatsApp:
      <a href="https://wa.me/${WA_NUMBER}" style="color:${ACCENT};text-decoration:none;font-weight:bold;">+1 782-802-6280</a>
    </p>
    <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;color:#555555;">Mit freundlichen Grüßen,<br><strong>Das IPTV Deutschland Team</strong></p>
  `);
}

function reminderEmail(name, username, password, m3uUrl) {
  const vorname = name && name !== "Nicht angegeben" ? name.split(" ")[0] : "";
  const greeting = vorname ? `Hallo ${vorname},` : "Hallo,";
  return emailWrap(`
    <p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:15px;color:#333333;">${greeting}</p>
    <p style="margin:0 0 14px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Ihr Testzugang <strong>läuft in 4 Stunden ab</strong> ⏳ — und ehrlich gesagt möchten wir Sie nicht verlieren.
    </p>
    <p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Sie haben echtes Streaming kennengelernt. Kristallklares 4K, Live-Sport vom ersten Moment an — Bundesliga, Sky Sport, DAZN — und eine Bibliothek so groß, dass Ihnen die Wochenenden ausgehen, bevor der Inhalt aufhört.
    </p>
    <p style="margin:0 0 22px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      <strong>Lassen Sie es nicht hier enden.</strong>
    </p>
    <p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Behalten Sie denselben Zugang. Behalten Sie dieselbe Qualität. Machen Sie es einfach dauerhaft.
    </p>
    ${replyJaBox()}
    <p style="margin:0 0 14px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Möchten Sie lieber zuerst unsere Pakete vergleichen?
    </p>
    ${ctaButton("Jetzt Abonnement wählen →", SITE_URL + "/iptv-preise.html")}
    <p style="margin:0 0 16px;font-family:Arial,sans-serif;font-size:14px;color:#555555;">Ihre aktiven Zugangsdaten:</p>
    ${credBox(username, password, m3uUrl)}
    <p style="margin:0 0 20px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Fragen? Antworten Sie auf diese E-Mail oder schreiben Sie uns auf WhatsApp:
      <a href="https://wa.me/${WA_NUMBER}" style="color:${ACCENT};text-decoration:none;font-weight:bold;">+1 782-802-6280</a> — wir sind immer für Sie da.
    </p>
    <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;color:#555555;">Mit freundlichen Grüßen,<br><strong>Das IPTV Deutschland Team</strong></p>
  `);
}

function followupEmail(name) {
  const vorname = name && name !== "Nicht angegeben" ? name.split(" ")[0] : "";
  const greeting = vorname ? `Hallo ${vorname},` : "Hallo,";
  return emailWrap(`
    <p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:15px;color:#333333;">${greeting}</p>
    <p style="margin:0 0 16px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Ihr Testzugang ist beendet — aber hier ist die Sache: <strong>Alles, was Sie gerade erlebt haben, wartet noch auf Sie.</strong>
    </p>
    <p style="margin:0 0 16px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Der Live-Sport. Die Spätabend-Filme. Das kristallklare 4K, das Ihren alten Streamingdienst wie einen schlechten Traum erscheinen ließ.
    </p>
    <p style="margin:0 0 22px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Alles davon — nur einen Klick entfernt.
    </p>
    <p style="margin:0 0 18px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      So machen Sie weiter — gleiche Qualität, keine Unterbrechung:
    </p>
    ${replyJaBox()}
    <p style="margin:0 0 14px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Möchten Sie Ihr Paket lieber selbst auswählen?
    </p>
    ${ctaButton("Mein Abonnement wählen →", SITE_URL + "/iptv-preise.html")}
    <p style="margin:0 0 20px;font-family:Arial,sans-serif;font-size:14px;line-height:1.65;color:#555555;">
      Eine Frage? Antworten Sie auf diese E-Mail oder schreiben Sie uns auf WhatsApp:
      <a href="https://wa.me/${WA_NUMBER}" style="color:${ACCENT};text-decoration:none;font-weight:bold;">+1 782-802-6280</a> — wir würden uns freuen, Sie zu behalten.
    </p>
    <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;color:#555555;">Mit freundlichen Grüßen,<br><strong>Das IPTV Deutschland Team</strong></p>
  `);
}

function adminEmail(name, email, country, device, whatsapp, notes, username, password, m3uUrl) {
  return `<!DOCTYPE html><html lang="de"><head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#333;padding:20px;">
  <h2 style="color:${ACCENT};margin-top:0;">Neuer Testzugang — IPTV Deutschland</h2>
  <table cellpadding="6" cellspacing="0" border="0">
    <tr><td style="color:#888;width:120px;">Name</td><td><strong>${name}</strong></td></tr>
    <tr><td style="color:#888;">E-Mail</td><td>${email}</td></tr>
    <tr><td style="color:#888;">Land</td><td>${country||"—"}</td></tr>
    <tr><td style="color:#888;">Gerät</td><td>${device||"—"}</td></tr>
    <tr><td style="color:#888;">WhatsApp</td><td>${whatsapp||"—"}</td></tr>
    <tr><td style="color:#888;">Nachricht</td><td>${notes||"—"}</td></tr>
    <tr><td colspan="2"><hr style="border:none;border-top:1px solid #eee;margin:8px 0;"></td></tr>
    <tr><td style="color:#888;">Benutzername</td><td><strong>${username}</strong></td></tr>
    <tr><td style="color:#888;">Passwort</td><td><strong>${password}</strong></td></tr>
    <tr><td style="color:#888;">M3U</td><td style="word-break:break-all;font-size:12px;">${m3uUrl}</td></tr>
  </table>
</body></html>`;
}

async function handleFetch(request, env) {
  if (request.method === "OPTIONS") {
    return new Response(null, { headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    }});
  }

  if (request.method === "GET") {
    const u = new URL(request.url);
    if (u.searchParams.has("debug")) {
      const bq = await apiGet({ action: "bouquet" });
      const trials = await env.TRIALS.list();
      return jsonRes({ bouquet: bq.text.slice(0,400), kv_keys: trials.keys.length });
    }
    return new Response("IPTV Deutschland Trial Worker — OK", { status: 200 });
  }

  if (request.method !== "POST") return jsonRes({ success: false, error: "POST only" }, 405);

  let body;
  try { body = await request.json(); }
  catch { return jsonRes({ success: false, error: "Ungültiges JSON" }, 400); }

  const { name, email, country, device, whatsapp, notes } = body;
  if (!email) return jsonRes({ success: false, error: "E-Mail erforderlich" }, 400);

  let step = "bouquet";
  try {
    const bqRes = await apiGet({ action: "bouquet" });
    let packId = "all";
    if (bqRes.text.trim().startsWith("[") || bqRes.text.trim().startsWith("{")) {
      const arr = JSON.parse(bqRes.text);
      const list = Array.isArray(arr) ? arr : Object.values(arr);
      const pkg = list.find(b => (b.name || "").trim().toLowerCase() === PACK_NAME.toLowerCase());
      if (pkg) packId = pkg.id;
    }

    step = "create_demo";
    const crRes = await apiGet({
      action: "new", type: "m3u", sub: "99", pack: packId,
      note: `Trial / iptvv.de / ${email} | ${whatsapp || ""}`,
    });
    if (!crRes.text.trim().startsWith("[") && !crRes.text.trim().startsWith("{")) {
      throw new Error(`Panel kein JSON: ${crRes.text.slice(0, 200)}`);
    }
    const crData = JSON.parse(crRes.text);
    const item = Array.isArray(crData) ? crData[0] : crData;
    if (!item || String(item.status) !== "true") {
      throw new Error(`Panel: ${item?.message || JSON.stringify(item)}`);
    }

    step = "extract";
    const rawUrl = item.url || "";
    let username = "", password = "";
    try { const u = new URL(rawUrl); username = u.searchParams.get("username") || ""; password = u.searchParams.get("password") || ""; } catch {}
    const m3uUrl = `${HOST}/get.php?username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&type=m3u_plus&output=ts`;

    step = "email_client";
    await sendEmail(email, "Ihr IPTV Deutschland Testzugang ist bereit – 24h Gratis aktiviert ✓", welcomeEmail(name, username, password, m3uUrl));

    step = "email_admin";
    await sendEmail(ADMIN_EMAIL, `Automation / iptvv.de / trial / ${name || "—"} / ${email}`, adminEmail(name, email, country, device, whatsapp, notes, username, password, m3uUrl));

    step = "kv_store";
    const expiry = Date.now() + 24 * 60 * 60 * 1000;
    await env.TRIALS.put(
      `trial:${email}`,
      JSON.stringify({ name, email, username, password, m3uUrl, expiry, reminder_sent: false, followup_sent: false }),
      { expirationTtl: 30 * 24 * 60 * 60 }
    );

    return jsonRes({ success: true });

  } catch (err) {
    console.error(`[step=${step}]`, err.message);
    return jsonRes({ success: false, error: `[${step}] ${err.message}` }, 500);
  }
}

async function handleScheduled(env) {
  const now = Date.now();
  const FOUR_HOURS = 4 * 60 * 60 * 1000;
  const { keys } = await env.TRIALS.list({ prefix: "trial:" });
  console.log(`[cron] ${keys.length} Tests geprüft`);

  for (const { name: key } of keys) {
    let trial;
    try { const raw = await env.TRIALS.get(key); if (!raw) continue; trial = JSON.parse(raw); } catch { continue; }
    const { name, email, username, password, m3uUrl, expiry, reminder_sent, followup_sent } = trial;

    if (!reminder_sent && now >= expiry - FOUR_HOURS && now < expiry) {
      try {
        await sendEmail(email, "⏳ Ihr IPTV Deutschland Testzugang läuft in 4 Stunden ab", reminderEmail(name, username, password, m3uUrl));
        trial.reminder_sent = true;
        await env.TRIALS.put(key, JSON.stringify(trial), { expirationTtl: 30 * 24 * 60 * 60 });
        console.log(`[cron] Erinnerung → ${email}`);
      } catch (e) { console.error(`[cron] Fehler Erinnerung:`, e.message); }
    }

    if (!followup_sent && now >= expiry) {
      try {
        await sendEmail(email, "Ihr IPTV Deutschland Testzugang ist abgelaufen — Jetzt weiterschauen 🎬", followupEmail(name));
        trial.followup_sent = true;
        await env.TRIALS.put(key, JSON.stringify(trial), { expirationTtl: 30 * 24 * 60 * 60 });
        console.log(`[cron] Nachfass → ${email}`);
      } catch (e) { console.error(`[cron] Fehler Nachfass:`, e.message); }
    }
  }
}

export default {
  async fetch(request, env) { return handleFetch(request, env); },
  async scheduled(event, env, ctx) { ctx.waitUntil(handleScheduled(env)); },
};

