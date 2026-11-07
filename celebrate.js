/* Full-screen success overlay after a free-trial request or a plan order.
   Load with <script src="/celebrate.js" data-kind="trial|order" defer></script>.
   It never touches the form or how it is sent: it remembers the e-mail on submit and shows the
   overlay as soon as the page reveals its own #formSuccessPanel.
   Preview without submitting: add ?celebrate=trial or ?celebrate=order to the page URL. */
(function () {
  var me = document.currentScript;
  var KIND = (me && me.getAttribute("data-kind")) || "trial";

  var TEXT = {
    trial: {
      title: "Ihr Gratis-Test ist unterwegs!",
      lines: [
        "Unsere Technik-Wichtel schicken Ihre Zugangsdaten gerade an <b data-c-email></b>, und zwar pünktlicher als jeder ICE. 🚄",
        "Das dauert meist keine 2 Minuten. Schauen Sie in Ihren <b>Posteingang</b> UND in Ihren <b>Spam-Ordner</b>, denn manchmal versteckt sich unsere Mail dort wie die Fernbedienung in der Sofaritze.",
        "Ihre einzige Aufgabe für die nächsten 24 Stunden: Chips holen. 🍿",
      ],
      btn: "Alles klar, ich hole die Chips",
    },
    order: {
      title: "Geschafft! Bestellung ist drin.",
      lines: [
        "Starke Entscheidung. Ihr Sofa wurde bereits informiert und ist mächtig stolz auf Sie. 🛋️",
        "Ihre Rechnung fliegt gerade an <b data-c-email></b>. Schauen Sie in Ihren <b>Posteingang</b> UND in Ihren <b>Spam-Ordner</b>, denn E-Mails spielen leider gern Verstecken.",
        "Rechnung bezahlen, und Ihre Sender laufen schneller an als ein Konter in der Nachspielzeit. ⚽",
      ],
      btn: "Super, los geht’s!",
    },
  };

  var CSS =
    ".iv-cel-on,.iv-cel-on body{overflow:hidden}" +
    ".iv-cel{position:fixed;inset:0;z-index:2147483000;display:grid;place-items:center;padding:16px;overflow-y:auto;font-family:Inter,system-ui,sans-serif;" +
    "background:radial-gradient(circle at 50% 35%,rgba(34,197,94,.22),transparent 60%),rgba(10,10,25,.92);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);animation:ivc-in .3s ease both}" +
    ".iv-cel.is-out{animation:ivc-out .25s ease forwards}" +
    ".iv-cel-box{position:relative;width:min(560px,100%);text-align:center;padding:clamp(28px,6vw,48px) clamp(18px,5vw,40px);color:#fff;" +
    "background:linear-gradient(160deg,#1b1b3a,#141428);border:1px solid rgba(34,197,94,.45);border-radius:22px;" +
    "box-shadow:0 0 0 1px rgba(34,197,94,.2),0 40px 120px -30px rgba(34,197,94,.45);animation:ivc-pop .55s .05s cubic-bezier(.2,.9,.3,1.3) both}" +
    ".iv-cel-x{position:absolute;top:10px;right:10px;width:44px;height:44px;border:0;border-radius:50%;background:rgba(255,255,255,.06);color:#9ca3af;font-size:28px;line-height:1;cursor:pointer}" +
    ".iv-cel-x:hover,.iv-cel-x:focus-visible{color:#fff;background:rgba(255,255,255,.12)}" +
    ".iv-cel-mark{display:block;width:clamp(130px,38vw,180px);height:auto;margin:0 auto 22px;fill:none;stroke:#4ade80;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 24px rgba(74,222,128,.5))}" +
    ".iv-cel-mark circle{stroke-width:6;stroke-dasharray:340;stroke-dashoffset:340;animation:ivc-draw .7s .2s ease forwards;fill:rgba(34,197,94,.1)}" +
    ".iv-cel-mark path{stroke-width:9;stroke-dasharray:80;stroke-dashoffset:80;animation:ivc-draw .45s .8s ease forwards,ivc-bounce .5s 1.2s ease;transform-origin:center}" +
    ".iv-cel h2{font-size:clamp(28px,6vw,40px);line-height:1.15;font-weight:900;margin:0 0 16px;color:#4ade80}" +
    ".iv-cel p{color:#c8cdd9;font-size:clamp(16px,2.2vw,18px);line-height:1.55;margin:0 auto 12px;max-width:460px}" +
    ".iv-cel p b{color:#fff;font-weight:800;word-break:break-word}" +
    ".iv-cel-go{display:block;margin:18px auto 0;width:100%;max-width:360px;padding:16px 22px;border:0;border-radius:14px;cursor:pointer;color:#fff;font:700 17px/1.2 Inter,system-ui,sans-serif;" +
    "background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);box-shadow:0 8px 26px rgba(102,126,234,.45);transition:transform .2s}" +
    ".iv-cel-go:hover{transform:translateY(-2px)}" +
    ".iv-cel-bits{position:fixed;inset:0;pointer-events:none;overflow:hidden}" +
    ".iv-cel-bits i{position:absolute;top:-40px;left:var(--x);width:10px;height:16px;border-radius:3px;font-style:normal;font-size:22px;line-height:1;" +
    "background:linear-gradient(135deg,#667eea,#764ba2);animation:ivc-fall var(--t) var(--d) linear infinite}" +
    ".iv-cel-bits i:nth-child(4n+1){background:#22c55e}.iv-cel-bits i:nth-child(4n+2){background:#f5af19}" +
    ".iv-cel-bits i:nth-child(3n+1){width:auto;height:auto;background:none}" +
    "@keyframes ivc-in{from{opacity:0}}@keyframes ivc-out{to{opacity:0}}" +
    "@keyframes ivc-pop{from{opacity:0;transform:scale(.85)}}@keyframes ivc-draw{to{stroke-dashoffset:0}}" +
    "@keyframes ivc-bounce{50%{transform:scale(1.15)}}" +
    "@keyframes ivc-fall{from{transform:translateY(0) rotate(var(--r))}to{transform:translateY(110vh) rotate(calc(var(--r) + 540deg))}}" +
    "@media (prefers-reduced-motion:reduce){.iv-cel,.iv-cel-box{animation:none}.iv-cel-bits{display:none}.iv-cel-mark circle,.iv-cel-mark path{animation:none;stroke-dashoffset:0}}";

  function addCss() {
    if (document.getElementById("iv-cel-css")) return;
    var s = document.createElement("style");
    s.id = "iv-cel-css";
    s.textContent = CSS;
    document.head.appendChild(s);
  }

  function celebrate(kind, email) {
    var c = TEXT[kind];
    if (!c) return;
    addCss();
    var old = document.querySelector(".iv-cel");
    if (old) old.remove();
    var back = document.activeElement;
    var el = document.createElement("div");
    el.className = "iv-cel";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    el.setAttribute("aria-labelledby", "iv-cel-title");
    var emoji = kind === "order" ? ["⚽", "🎉", "🍺"] : ["🍿", "🎉", "📺"];
    var bits = "";
    for (var i = 0; i < 28; i++) {
      bits += '<i style="--x:' + ((i * 37) % 100) + "%;--d:" + (i % 7) * 0.35 + "s;--t:" + (3.2 + (i % 5) * 0.5) + "s;--r:" + ((i * 53) % 360) + 'deg">' +
        (i % 3 ? "" : emoji[(i / 3) % 3]) + "</i>";
    }
    el.innerHTML =
      '<div class="iv-cel-bits" aria-hidden="true">' + bits + "</div>" +
      '<div class="iv-cel-box">' +
      '<button class="iv-cel-x" type="button" aria-label="Schließen">×</button>' +
      '<svg class="iv-cel-mark" viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="54"/><path d="M36 62 53 79 86 44"/></svg>' +
      '<h2 id="iv-cel-title">' + c.title + "</h2>" +
      c.lines.map(function (l) { return "<p>" + l + "</p>"; }).join("") +
      '<button class="iv-cel-go" type="button">' + c.btn + "</button>" +
      "</div>";
    el.querySelectorAll("[data-c-email]").forEach(function (b) { b.textContent = email || "Ihre E-Mail-Adresse"; });
    var go = el.querySelector(".iv-cel-go"), x = el.querySelector(".iv-cel-x");
    function onKey(e) {
      if (e.key === "Escape") close();
      if (e.key === "Tab") { e.preventDefault(); (document.activeElement === go ? x : go).focus(); }
    }
    function close() {
      document.removeEventListener("keydown", onKey);
      el.classList.add("is-out");
      document.documentElement.classList.remove("iv-cel-on");
      setTimeout(function () { el.remove(); }, 250);
      var panel = document.getElementById("formSuccessPanel");
      if (panel && !panel.classList.contains("hidden")) panel.scrollIntoView({ block: "center" });
      else if (back && back.focus) back.focus({ preventScroll: true });
    }
    document.addEventListener("keydown", onKey);
    x.addEventListener("click", close);
    go.addEventListener("click", close);
    document.body.appendChild(el);
    document.documentElement.classList.add("iv-cel-on");
    go.focus({ preventScroll: true });
  }
  window.ivCelebrate = celebrate;

  // Remember the address on submit (the page resets the form after a successful send).
  var lastEmail = "";
  document.addEventListener("submit", function (e) {
    var f = e.target, inp = f && f.querySelector && f.querySelector("#email, input[type=email], input[name=email]");
    if (inp && inp.value) lastEmail = inp.value.trim();
  }, true);

  // Show the overlay when the page reveals its own success panel.
  var panel = document.getElementById("formSuccessPanel");
  if (panel && window.MutationObserver) {
    var wasHidden = panel.classList.contains("hidden");
    new MutationObserver(function () {
      var hidden = panel.classList.contains("hidden");
      if (wasHidden && !hidden) celebrate(KIND, lastEmail);
      wasHidden = hidden;
    }).observe(panel, { attributes: true, attributeFilter: ["class"] });
  }

  var q = new URLSearchParams(location.search).get("celebrate");
  if (q) celebrate(q === "order" ? "order" : "trial", "sie@beispiel.de");
})();
