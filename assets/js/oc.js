/* Official Creations — shared site behaviour. Vanilla JS, no dependencies. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.remove("no-js");

  /* Mobile navigation */
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  var setNavOpen = function () {};
  if (toggle && links) {
    setNavOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      links.classList.toggle("open", open);
    };
    toggle.addEventListener("click", function () {
      setNavOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setNavOpen(false);
    });
    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNavOpen(false);
    });
  }

  /* Scroll reveals (used sparingly) */
  var targets = document.querySelectorAll("[data-reveal], .step");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          var delay = en.target.getAttribute("data-delay");
          if (delay) en.target.style.transitionDelay = delay + "ms";
          en.target.classList.add("in");
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.2, rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (t) { io.observe(t); });
  } else {
    targets.forEach(function (t) { t.classList.add("in"); });
  }

  /* Interactive ecosystem map (hero card and Our Ecosystem page) */
  document.querySelectorAll("[data-map]").forEach(function (map) {
    var nodes = map.querySelectorAll(".node");
    var panel = map.querySelector(".map-panel");
    if (!panel) return;
    var title = panel.querySelector("h3");
    var text = panel.querySelector("p");
    var more = panel.querySelector("a");
    var base = { t: title.textContent, p: text.textContent };

    function activate(node) {
      nodes.forEach(function (n) { n.classList.toggle("on", n === node); });
      title.textContent = node.getAttribute("data-title");
      text.textContent = node.getAttribute("data-text");
      if (more) {
        more.setAttribute("href", node.getAttribute("data-href"));
        more.firstChild.textContent = node.getAttribute("data-link") + " ";
        more.hidden = false;
      }
    }
    function reset() {
      nodes.forEach(function (n) { n.classList.remove("on"); });
      title.textContent = base.t;
      text.textContent = base.p;
      if (more) more.hidden = true;
    }
    nodes.forEach(function (n) {
      n.addEventListener("mouseenter", function () { activate(n); });
      n.addEventListener("focus", function () { activate(n); });
      n.addEventListener("click", function (e) {
        // First tap previews on touch screens; second tap follows the link.
        if (!n.classList.contains("on")) { e.preventDefault(); activate(n); }
      });
    });
    map.addEventListener("mouseleave", function () {
      if (!map.contains(document.activeElement) || document.activeElement === document.body) reset();
    });
    if (more) more.hidden = true;
  });

  /* Booking sheet: every "Book a Consultation" link opens the form directly.
     Without dialog support, or without JavaScript, the link goes to book.html. */
  var sheet = document.getElementById("book-sheet");
  var lastTrigger = null;
  var canSheet = !!(sheet && typeof sheet.showModal === "function");
  if (canSheet) {
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a[data-book]");
      if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      setNavOpen(false);
      lastTrigger = a;
      if (!sheet.open) sheet.showModal();
      root.classList.add("sheet-open");
    });
    sheet.addEventListener("click", function (e) {
      if (e.target === sheet || e.target.closest("[data-close]")) sheet.close();
    });
    sheet.addEventListener("close", function () {
      root.classList.remove("sheet-open");
      if (lastTrigger && document.contains(lastTrigger)) { try { lastTrigger.focus({ preventScroll: true }); } catch (err) {} }
    });
  }

  /* Consultation forms: open a prefilled email. No backend. */
  document.querySelectorAll("form.consult").forEach(function (form) {
    var msg = form.querySelector(".form-msg");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var to = form.getAttribute("data-to") || "";
      var pub = form.getAttribute("data-public") || to;
      var d = new FormData(form);
      var val = function (k, fallback) { var v = d.get(k); return v ? String(v) : (fallback || ""); };
      var suggest = val("suggest").replace("T", " at ");
      var lines = [
        "Name: " + val("name"),
        "Business: " + val("business", "-"),
        "Email: " + val("email"),
        "Website or social page: " + val("site", "-"),
        "Interested in: " + val("interest", "-"),
        "Suggested time: " + (suggest || "-"),
        "",
        "Where the business is today and what's getting in the way:",
        val("challenge")
      ];
      if (!to || to.indexOf("REPLACE_ME") !== -1) {
        msg.textContent = "The consultation email address hasn't been set up yet. Add it in site.config.json and rebuild.";
        msg.classList.add("show");
        return;
      }
      var subject = "Consultation request: " + (val("business") || val("name"));
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      msg.textContent = "Your email app should open with the message ready to send. If nothing opens, email us at " + pub + ".";
      msg.classList.add("show");
    });
  });

  var yr = document.getElementById("yr");
  if (yr) yr.textContent = String(new Date().getFullYear());
})();
