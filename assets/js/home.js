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


  /* Offline to online story: layers in depth.
     Tablet and desktop: pinned, scroll-driven, damped. Phones: Offline / Online buttons, no scroll motion. */
  (function () {
    var story = document.querySelector("[data-story]");
    if (!story) return;
    var scene = story.querySelector(".story-scene");
    var wrap = story.closest(".wrap");
    var layers = Array.prototype.slice.call(story.querySelectorAll(".ly"));
    var buttons = Array.prototype.slice.call(story.querySelectorAll(".sw"));
    var phone = window.matchMedia("(max-width: 699px)");
    var target = 0, shown = 0, last = 0, raf = 0, ready = false;

    var ease = function (t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
    var easeOut = function (t) { return 1 - Math.pow(1 - t, 3); };
    var back = function (t) { var c1 = 1.15, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
    var seg = function (p, a, b) { return clamp((p - a) / (b - a)); };

    /* One value, p (0 to 1), drives everything, so forward and reverse always match. */
    function render(p) {
      var tilt = ease(seg(p, 0, .2)) * (1 - ease(seg(p, .78, 1)));
      var lift = easeOut(seg(p, .2, .5)) * (1 - ease(seg(p, .78, 1)));
      scene.style.setProperty("--tilt", tilt.toFixed(4));
      scene.style.setProperty("--lift", lift.toFixed(4));
      scene.style.setProperty("--off", (1 - seg(p, .38, .52)).toFixed(3));
      scene.style.setProperty("--on", ease(seg(p, .6, .78)).toFixed(3));
      for (var i = 0; i < layers.length; i++) {
        var s = .4 + i * .05;
        layers[i].style.setProperty("--m", back(seg(p, s, s + .3)).toFixed(4));
      }
    }

    /* Raw scroll position to 0..1. Pinned: progress through the stuck distance, with small hold zones at both ends. */
    function measure() {
      var h = vh();
      var panel = story.getBoundingClientRect();
      var top = parseFloat(getComputedStyle(story).top);
      if (isNaN(top)) top = 0;
      var fits = panel.height <= h - top - 12;
      story.classList.toggle("nopin", !fits);
      wrap.classList.toggle("nopin", !fits);
      if (fits) {
        var r = wrap.getBoundingClientRect();
        var raw = (top - r.top) / Math.max(1, r.height - panel.height);
        return clamp((raw - .04) / .9);
      }
      var s = scene.getBoundingClientRect();
      return clamp((h * .85 - s.top) / (h * .6));
    }

    function frame(t) {
      var dt = Math.min(.1, (t - last) / 1000 || .016); last = t;
      shown += (target - shown) * (1 - Math.exp(-dt * 11));
      if (Math.abs(target - shown) < .0008) shown = target;
      render(shown);
      raf = shown === target ? 0 : requestAnimationFrame(frame);
    }
    function kick() {
      target = measure();
      if (!raf) { last = performance.now(); raf = requestAnimationFrame(frame); }
    }

    function setPhone(on) {
      scene.classList.toggle("is-online", on);
      buttons.forEach(function (b) { b.setAttribute("aria-pressed", String((b.getAttribute("data-state") === "on") === on)); });
    }

    function mode() {
      window.removeEventListener("scroll", kick);
      window.removeEventListener("resize", kick);
      var props = ["--tilt", "--lift", "--off", "--on"];
      if (phone.matches) {
        props.forEach(function (n) { scene.style.removeProperty(n); });
        layers.forEach(function (l) { l.style.removeProperty("--m"); });
        story.classList.remove("nopin"); wrap.classList.remove("nopin");
        return;
      }
      scene.classList.remove("is-online");
      if (reduce) { render(1); return; }
      window.addEventListener("scroll", kick, { passive: true });
      window.addEventListener("resize", kick);
      shown = target = measure();
      render(shown);
    }

    buttons.forEach(function (b) {
      b.addEventListener("click", function () { setPhone(b.getAttribute("data-state") === "on"); });
    });
    if (phone.addEventListener) phone.addEventListener("change", mode); else if (phone.addListener) phone.addListener(mode);
    mode();
    ready = true;
  })();

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
