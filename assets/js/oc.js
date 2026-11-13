/* Official Creations — site behaviour. Vanilla JS, no dependencies. */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.remove("no-js");

  /* Mobile navigation */
  var toggle = document.querySelector(".nav-toggle");
  var links = document.getElementById("nav-links");
  if (toggle && links) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      links.classList.toggle("open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
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

  /* Interactive ecosystem map */
  document.querySelectorAll("[data-map]").forEach(function (map) {
    var nodes = map.querySelectorAll(".node");
    var panel = map.querySelector(".map-panel");
    if (!panel) return;
    var title = panel.querySelector("h3");
    var text = panel.querySelector("p");
    var more = panel.querySelector("a");
    var base = { t: title.textContent, p: text.textContent, h: more ? more.getAttribute("href") : "", l: more ? more.textContent : "" };

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

  /* Consultation form: opens a prefilled email. No backend. */
  var form = document.getElementById("consult-form");
  if (form) {
    var msg = form.querySelector(".form-msg");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var to = form.getAttribute("data-to") || "";
      var d = new FormData(form);
      var lines = [
        "Name: " + (d.get("name") || ""),
        "Business: " + (d.get("business") || ""),
        "Email: " + (d.get("email") || ""),
        "Website or social page: " + (d.get("site") || "-"),
        "Interested in: " + (d.get("interest") || ""),
        "",
        "Where the business is today and what's getting in the way:",
        (d.get("challenge") || "")
      ];
      if (!to || to.indexOf("REPLACE_ME") !== -1) {
        msg.textContent = "The consultation email address hasn't been set up yet. Add it in site.config.json and rebuild.";
        msg.classList.add("show");
        return;
      }
      var subject = "Consultation request: " + (d.get("business") || d.get("name") || "");
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(lines.join("\n"));
      msg.textContent = "Your email app should open with the message ready to send. If nothing opens, email us directly at " + to + ".";
      msg.classList.add("show");
    });
  }
})();
