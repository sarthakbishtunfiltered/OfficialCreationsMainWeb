/* Official Creations — homepage motion. Vanilla JS, no libraries.
   Without JS or with reduced motion, every section shows its finished state. */
(function () {
  "use strict";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var clamp = function (v) { return Math.max(0, Math.min(1, v)); };
  var vh = function () { return window.innerHeight || document.documentElement.clientHeight; };

  /* Kinetic headlines: wrap each word, reveal when scrolled into view. */
  var heads = document.querySelectorAll("[data-kinetic]");
  if (!reduce && "IntersectionObserver" in window) {
    var kio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); kio.unobserve(en.target); }
      });
    }, { threshold: 0.35 });
    heads.forEach(function (el) {
      var text = el.textContent.trim();
      el.setAttribute("aria-label", text);
      el.textContent = "";
      text.split(/\s+/).forEach(function (w, i, all) {
        var outer = document.createElement("span");
        outer.className = "kw";
        outer.setAttribute("aria-hidden", "true");
        var inner = document.createElement("span");
        inner.style.setProperty("--i", i);
        inner.textContent = w;
        outer.appendChild(inner);
        el.appendChild(outer);
        if (i < all.length - 1) el.appendChild(document.createTextNode(" "));
      });
      el.classList.add("k-ready");
      kio.observe(el);
    });
  }

  /* Scroll-driven pieces share one rAF loop. */
  var pars = reduce ? [] : Array.prototype.slice.call(document.querySelectorAll("[data-par]"));
  var story = document.querySelector("[data-story]");
  var draw = document.querySelector("[data-draw]");
  var clip = draw && draw.querySelector(".pclip");
  var stops = draw ? Array.prototype.slice.call(draw.querySelectorAll(".pstop")) : [];
  var stopY = [12.5, 37.5, 62.5, 87.5];
  if (draw && !reduce) draw.classList.add("armed");
  var ticking = false;

  function update() {
    ticking = false;
    var h = vh();

    pars.forEach(function (el) {
      var host = el.parentElement.getBoundingClientRect();
      var mid = host.top + host.height / 2 - h / 2;
      var speed = parseFloat(el.getAttribute("data-par")) || 0;
      el.style.transform = "translate3d(0," + (-mid * speed).toFixed(1) + "px,0)";
    });

    if (story && !reduce) {
      var desktop = window.innerWidth >= 1000;
      var p;
      if (desktop) {
        var wrap = story.closest(".wrap");
        var r = wrap.getBoundingClientRect();
        p = clamp(-r.top / Math.max(1, r.height - h * 0.9) * 1.15 + 0.02);
      } else {
        var s = story.querySelector(".story-scene").getBoundingClientRect();
        p = clamp((h * 0.85 - s.top) / (h * 0.55));
      }
      story.style.setProperty("--p", p.toFixed(3));
    }

    if (draw && clip && !reduce) {
      var d = draw.getBoundingClientRect();
      var f = clamp((h * 0.62 - d.top) / d.height);
      clip.setAttribute("height", (f * 102).toFixed(2));
      stops.forEach(function (s2, i) { s2.classList.toggle("on", f * 100 >= stopY[i] - 1); });
    }
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(update); } }
  if (!reduce) {
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
  }
  update();

  /* Ecosystem constellation: pick a shape to focus it and its connections. */
  document.querySelectorAll("[data-const]").forEach(function (root) {
    var stage = root.querySelector(".cstage");
    var nodes = Array.prototype.slice.call(root.querySelectorAll(".cnode"));
    var lines = Array.prototype.slice.call(root.querySelectorAll(".cline"));
    var box = root.querySelector(".cdetail");
    var title = box.querySelector("h3");
    var text = box.querySelector("p");
    var more = box.querySelector("a");
    var base = { t: title.textContent, p: text.textContent, h: more.getAttribute("href"), l: more.firstChild.textContent };
    var current = null;

    function show(node) {
      current = node;
      var links = (node.getAttribute("data-links") || "").split(",");
      var idx = node.getAttribute("data-i");
      stage.classList.add("has-sel");
      nodes.forEach(function (n) {
        n.classList.toggle("on", n === node);
        n.classList.toggle("rel", links.indexOf(n.getAttribute("data-i")) !== -1);
        n.setAttribute("aria-pressed", String(n === node));
      });
      lines.forEach(function (l) {
        l.classList.toggle("hot", l.getAttribute("data-a") === idx || l.getAttribute("data-b") === idx);
      });
      title.textContent = node.getAttribute("data-title");
      text.textContent = node.getAttribute("data-text");
      more.setAttribute("href", node.getAttribute("data-href"));
      more.firstChild.textContent = node.getAttribute("data-link") + " ";
    }
    function clear() {
      current = null;
      stage.classList.remove("has-sel");
      nodes.forEach(function (n) { n.classList.remove("on", "rel"); n.setAttribute("aria-pressed", "false"); });
      lines.forEach(function (l) { l.classList.remove("hot"); });
      title.textContent = base.t; text.textContent = base.p;
      more.setAttribute("href", base.h); more.firstChild.textContent = base.l;
    }
    nodes.forEach(function (n) {
      n.setAttribute("aria-pressed", "false");
      n.addEventListener("click", function (e) { e.stopPropagation(); if (current === n && !window.matchMedia("(hover: hover)").matches) clear(); else show(n); });
      n.addEventListener("mouseenter", function () { if (window.matchMedia("(hover: hover)").matches) show(n); });
    });
    stage.addEventListener("mouseleave", function () {
      if (window.matchMedia("(hover: hover)").matches && !stage.contains(document.activeElement)) clear();
    });
  });
})();
