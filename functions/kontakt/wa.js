// Cloudflare Pages Function
// Route: /kontakt/wa
//
// Keeps the real WhatsApp number out of this site's HTML source.
// Buttons link here instead of directly to wa.me/<number>; this function
// 302-redirects the visitor straight to WhatsApp.
//
// To change the number later, edit WHATSAPP_NUMBER below and push.

const WHATSAPP_NUMBER = '17828026280'; // digits only, no +, spaces or dashes

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const msg = url.searchParams.get('msg');

  const target = msg
    ? `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`
    : `https://wa.me/${WHATSAPP_NUMBER}`;

  return Response.redirect(target, 302);
}
