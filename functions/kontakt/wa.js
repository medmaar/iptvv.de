// Cloudflare Pages Function
// Route: /kontakt/wa
//
// Keeps the real WhatsApp number out of this site's HTML source. Buttons
// link here instead of directly to wa.me/<number>; this function
// 302-redirects the visitor straight to WhatsApp.
//
// It also ALWAYS prepends a brand tag to the pre-filled message, no matter
// what each button passes in ?msg=. Since every site forwards to the same
// personal WhatsApp inbox, this is how Mo can tell which site a lead came
// from just by reading the first line of the chat.
//
// To change the number or brand tag later, edit the two constants below
// and push - no need to touch any page.

const WHATSAPP_NUMBER = '17828026280'; // digits only, no +, spaces or dashes
const BRAND_GREETING = 'Hallo IPTV Deutschland!';

function buildMessage(raw) {
  if (!raw) return BRAND_GREETING;
  let rest = raw.replace(/^Hallo[^!.,]*[!,.]?\s*/i, '').trim();
  if (rest) {
    rest = rest.charAt(0).toUpperCase() + rest.slice(1);
    return `${BRAND_GREETING} ${rest}`;
  }
  return BRAND_GREETING;
}

export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const msg = url.searchParams.get('msg');
  const finalMsg = buildMessage(msg);

  const target = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(finalMsg)}`;

  return Response.redirect(target, 302);
}
