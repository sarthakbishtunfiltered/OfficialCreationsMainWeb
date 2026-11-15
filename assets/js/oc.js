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

  /* Custom dropdowns and date/time picker. The native controls stay in the form (and work without JS);
     these replace them visually and write the chosen value back, so submission is unchanged. */
  var CHEV = '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M5 8l5 5 5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var closers = [];
  function closeAll(except) { closers.forEach(function (c) { if (c !== except) c(); }); }
  document.addEventListener("click", function (e) { closers.forEach(function (c) { c(e.target); }); });

  document.querySelectorAll(".field select").forEach(function (sel) {
    var field = sel.parentNode, id = sel.id;
    var wrap = document.createElement("div"); wrap.className = "cs";
    var btn = document.createElement("button"); btn.type = "button"; btn.className = "cs-btn"; btn.id = id;
    btn.setAttribute("aria-haspopup", "listbox"); btn.setAttribute("aria-expanded", "false");
    var list = document.createElement("ul"); list.className = "cs-list"; list.setAttribute("role", "listbox"); list.hidden = true;
    list.id = id + "-list"; btn.setAttribute("aria-controls", list.id);
    var opts = Array.prototype.slice.call(sel.options);
    var cur = Math.max(0, sel.selectedIndex), active = cur;
    opts.forEach(function (o, i) {
      var li = document.createElement("li"); li.setAttribute("role", "option"); li.id = id + "-o" + i;
      li.innerHTML = '<span></span><svg viewBox="0 0 20 20" width="16" height="16" aria-hidden="true"><path d="M4 10.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
      li.firstChild.textContent = o.textContent;
      li.addEventListener("click", function (e) { e.stopPropagation(); choose(i); close(); btn.focus(); });
      li.addEventListener("mousemove", function () { setActive(i); });
      list.appendChild(li);
    });
    function paint() {
      btn.innerHTML = "<span></span>" + CHEV; btn.firstChild.textContent = opts[cur].textContent;
      Array.prototype.forEach.call(list.children, function (li, i) { li.setAttribute("aria-selected", String(i === cur)); li.classList.toggle("act", i === active); });
    }
    function setActive(i) { active = Math.max(0, Math.min(opts.length - 1, i)); btn.setAttribute("aria-activedescendant", id + "-o" + active); paint(); }
    function choose(i) { cur = active = i; sel.selectedIndex = i; sel.dispatchEvent(new Event("change", { bubbles: true })); paint(); }
    function open() { closeAll(close); list.hidden = false; btn.setAttribute("aria-expanded", "true"); active = cur; setActive(cur); }
    function close(t) {
      if (t && t.nodeType && wrap.contains(t)) return;
      list.hidden = true; btn.setAttribute("aria-expanded", "false"); btn.removeAttribute("aria-activedescendant");
    }
    closers.push(close);
    btn.addEventListener("click", function (e) { e.stopPropagation(); if (list.hidden) open(); else close(); });
    btn.addEventListener("keydown", function (e) {
      var k = e.key;
      if (list.hidden) {
        if (k === "ArrowDown" || k === "ArrowUp") { e.preventDefault(); open(); }
        return;
      }
      if (k === "ArrowDown") { e.preventDefault(); setActive(active + 1); }
      else if (k === "ArrowUp") { e.preventDefault(); setActive(active - 1); }
      else if (k === "Home") { e.preventDefault(); setActive(0); }
      else if (k === "End") { e.preventDefault(); setActive(opts.length - 1); }
      else if (k === "Enter" || k === " ") { e.preventDefault(); choose(active); close(); }
      else if (k === "Escape") { e.preventDefault(); e.stopPropagation(); close(); }
      else if (k === "Tab") close();
    });
    sel.removeAttribute("id"); sel.tabIndex = -1; sel.setAttribute("aria-hidden", "true"); sel.classList.add("native-hidden");
    wrap.appendChild(btn); wrap.appendChild(list); field.appendChild(wrap);
    sel.form && sel.form.addEventListener("reset", function () { setTimeout(function () { cur = active = sel.selectedIndex; paint(); }, 0); });
    paint();
  });

  var MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  var DAYS = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"];
  var pad = function (n) { return (n < 10 ? "0" : "") + n; };
  var iso = function (d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); };

  document.querySelectorAll('.field input[type="datetime-local"]').forEach(function (inp) {
    var field = inp.parentNode, id = inp.id;
    var wrap = document.createElement("div"); wrap.className = "cp";
    var btn = document.createElement("button"); btn.type = "button"; btn.className = "cp-btn"; btn.id = id;
    btn.setAttribute("aria-haspopup", "dialog"); btn.setAttribute("aria-expanded", "false");
    var panel = document.createElement("div"); panel.className = "cp-panel"; panel.hidden = true; panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "Choose a date and time");
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var view = new Date(today.getFullYear(), today.getMonth(), 1);
    var pickDate = null, tH = 10, tM = 0, tP = "AM", timeSet = false;
    var ICON = '<svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><rect x="2.5" y="4" width="15" height="13" rx="3" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M2.5 8.5h15M6.5 2.5v3M13.5 2.5v3" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>';
    var h24 = function () { return (tH % 12) + (tP === "PM" ? 12 : 0); };
    var fmt = function () { return tH + ":" + pad(tM) + " " + tP; };

    function isPast() {
      if (!pickDate || iso(pickDate) !== iso(new Date())) return false;
      var n = new Date(); return h24() * 60 + tM <= n.getHours() * 60 + n.getMinutes();
    }
    function label() {
      btn.innerHTML = ICON;
      var s = document.createElement("span");
      if (pickDate && timeSet) { s.textContent = pickDate.toLocaleDateString(undefined, { weekday: "short", day: "numeric", month: "short" }) + " · " + fmt(); }
      else { s.textContent = "Pick a date and time"; s.className = "ph"; }
      btn.appendChild(s);
    }
    function commit() {
      inp.value = (pickDate && timeSet && !isPast()) ? iso(pickDate) + "T" + pad(h24()) + ":" + pad(tM) : "";
      label();
    }
    function wheel(name, values, current) {
      var h = '<ul class="cp-wheel" tabindex="0" role="listbox" aria-label="' + name + '" data-w="' + name + '">';
      values.forEach(function (v) { h += '<li role="option" data-v="' + v + '"' + (String(v) === String(current) ? ' class="sel" aria-selected="true"' : "") + ">" + (typeof v === "number" && name === "Minute" ? pad(v) : v) + "</li>"; });
      return h + "</ul>";
    }
    function status() {
      var warn = panel.querySelector(".cp-warn"), done = panel.querySelector(".cp-done"), past = isPast();
      if (warn) warn.textContent = past ? "That time has already passed today." : "";
      if (done) done.disabled = !(pickDate && timeSet) || past;
    }
    function render() {
      var y = view.getFullYear(), m = view.getMonth();
      var first = (new Date(y, m, 1).getDay() + 6) % 7, count = new Date(y, m + 1, 0).getDate();
      var canPrev = y > today.getFullYear() || m > today.getMonth();
      var h = '<div class="cp-head"><button type="button" class="cp-nav" data-nav="-1" aria-label="Previous month"' + (canPrev ? "" : " disabled") + '>‹</button>' +
        '<strong aria-live="polite">' + MONTHS[m] + " " + y + '</strong><button type="button" class="cp-nav" data-nav="1" aria-label="Next month">›</button></div>';
      h += '<div class="cp-grid" role="grid">' + DAYS.map(function (d) { return '<span class="cp-dow">' + d + "</span>"; }).join("");
      for (var i = 0; i < first; i++) h += "<span></span>";
      for (var d = 1; d <= count; d++) {
        var dt = new Date(y, m, d), past = dt < today, sel = pickDate && iso(dt) === iso(pickDate), isToday = iso(dt) === iso(today);
        h += '<button type="button" class="cp-day' + (sel ? " sel" : "") + (isToday ? " today" : "") + '" data-d="' + iso(dt) + '"' + (past ? " disabled" : "") +
          ' aria-pressed="' + (sel ? "true" : "false") + '" aria-label="' + dt.toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long", year: "numeric" }) + '">' + d + "</button>";
      }
      h += "</div>";
      var hrs = [], mins = []; for (var a = 1; a <= 12; a++) hrs.push(a); for (var b2 = 0; b2 < 60; b2++) mins.push(b2);
      h += '<p class="cp-time-h">' + (pickDate ? "Time on " + pickDate.toLocaleDateString(undefined, { weekday: "long", day: "numeric", month: "long" }) : "Pick a day, then scroll to set the time") + "</p>";
      h += '<div class="cp-wheels">' + wheel("Hour", hrs, tH) + wheel("Minute", mins, tM) + wheel("Period", ["AM", "PM"], tP) + "</div>";
      h += '<p class="cp-warn" role="status"></p>';
      h += '<div class="cp-foot"><span>Your local time</span><div><button type="button" class="cp-clear" data-clear>Clear</button><button type="button" class="cp-done" data-done>Done</button></div></div>';
      panel.innerHTML = h;
      var tw = panel.querySelector(".cp-wheels"); tw.style.opacity = pickDate ? "1" : ".45"; tw.style.pointerEvents = pickDate ? "" : "none";
      sync(true); status();
    }
    var ih = function (w) { return w.children[0].getBoundingClientRect().height || 37; };
    function sync(instant) {
      panel.querySelectorAll(".cp-wheel").forEach(function (w) {
        var cur = w.getAttribute("data-w") === "Hour" ? tH : w.getAttribute("data-w") === "Minute" ? tM : tP;
        var items = w.children;
        for (var i = 0; i < items.length; i++) {
          if (String(items[i].getAttribute("data-v")) === String(cur)) { w.scrollTo({ top: i * ih(w), behavior: instant ? "auto" : "smooth" }); break; }
        }
      });
    }
    function readWheel(w) {
      var items = w.children, idx = Math.max(0, Math.min(items.length - 1, Math.round(w.scrollTop / ih(w))));
      /* If the wheel came to rest between two values, nudge it so the chosen value sits exactly in the band. */
      var want = idx * ih(w);
      if (Math.abs(w.scrollTop - want) > 1) w.scrollTo({ top: want, behavior: "smooth" });
      var v = items[idx].getAttribute("data-v"), name = w.getAttribute("data-w");
      Array.prototype.forEach.call(items, function (li, i) { li.classList.toggle("sel", i === idx); li.setAttribute("aria-selected", String(i === idx)); });
      if (name === "Hour") tH = +v; else if (name === "Minute") tM = +v; else tP = v;
      timeSet = true; commit(); status();
    }
    function open() { closeAll(close); if (pickDate) view = new Date(pickDate.getFullYear(), pickDate.getMonth(), 1); render(); panel.hidden = false; btn.setAttribute("aria-expanded", "true"); sync(true); }
    function close(t) {
      if (t && t.nodeType && wrap.contains(t)) return;
      if (panel.hidden) return;
      panel.hidden = true; btn.setAttribute("aria-expanded", "false");
    }
    closers.push(close);
    btn.addEventListener("click", function (e) { e.stopPropagation(); if (panel.hidden) open(); else close(); });
    var settle = null;
    panel.addEventListener("scroll", function (e) {
      var w = e.target; if (!w.classList || !w.classList.contains("cp-wheel")) return;
      clearTimeout(settle); settle = setTimeout(function () { readWheel(w); }, 90);
    }, true);
    panel.addEventListener("click", function (e) {
      e.stopPropagation();
      var li = e.target.closest(".cp-wheel li");
      if (li) { var w = li.parentNode; w.scrollTo({ top: Array.prototype.indexOf.call(w.children, li) * ih(w), behavior: "smooth" }); return; }
      var t = e.target.closest("button"); if (!t || t.disabled) return;
      if (t.hasAttribute("data-nav")) { view = new Date(view.getFullYear(), view.getMonth() + parseInt(t.getAttribute("data-nav"), 10), 1); render(); var n = panel.querySelector('[data-nav="' + t.getAttribute("data-nav") + '"]'); if (n && !n.disabled) n.focus(); return; }
      if (t.hasAttribute("data-clear")) { pickDate = null; timeSet = false; tH = 10; tM = 0; tP = "AM"; commit(); render(); return; }
      if (t.hasAttribute("data-done")) { close(); btn.focus(); return; }
      if (t.hasAttribute("data-d")) {
        var p = t.getAttribute("data-d").split("-"); pickDate = new Date(+p[0], +p[1] - 1, +p[2]);
        if (!timeSet) {
          var n2 = new Date(), hr = 10;
          if (iso(pickDate) === iso(n2)) hr = Math.min(n2.getHours() + 1, 23);
          tP = hr >= 12 ? "PM" : "AM"; tH = hr % 12 === 0 ? 12 : hr % 12; tM = 0; timeSet = true;
        }
        commit(); render();
        var again = panel.querySelector('[data-d="' + t.getAttribute("data-d") + '"]'); if (again) again.focus();
      }
    });
    panel.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); close(); btn.focus(); return; }
      var t = e.target;
      if (t.classList && t.classList.contains("cp-wheel")) {
        var d = e.key === "ArrowDown" ? 1 : e.key === "ArrowUp" ? -1 : 0;
        if (d) { e.preventDefault(); t.scrollBy({ top: d * ih(t), behavior: "smooth" }); }
        return;
      }
      if (t.classList && t.classList.contains("cp-day")) {
        var delta = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -7, ArrowDown: 7 }[e.key];
        if (delta) {
          e.preventDefault();
          var days = Array.prototype.slice.call(panel.querySelectorAll(".cp-day"));
          var i = days.indexOf(t) + delta;
          while (i >= 0 && i < days.length && days[i].disabled) i += delta > 0 ? 1 : -1;
          if (days[i]) days[i].focus();
        }
      }
    });
    inp.type = "hidden"; inp.removeAttribute("id");
    if (inp.value) { var m0 = inp.value.match(/^(\d+)-(\d+)-(\d+)T(\d+):(\d+)/); if (m0) { pickDate = new Date(+m0[1], +m0[2] - 1, +m0[3]); var hh0 = +m0[4]; tP = hh0 >= 12 ? "PM" : "AM"; tH = hh0 % 12 === 0 ? 12 : hh0 % 12; tM = +m0[5]; timeSet = true; } }
    wrap.appendChild(btn); wrap.appendChild(panel); field.appendChild(wrap);
    inp.form && inp.form.addEventListener("reset", function () { pickDate = null; timeSet = false; commit(); });
    label();
  });

  /* Consultation forms: open a prefilled email. No backend. */
  document.querySelectorAll("form.consult").forEach(function (form) {
    var msg = form.querySelector(".form-msg");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var to = form.getAttribute("data-to") || "";
      var pub = form.getAttribute("data-public") || to;
      var d = new FormData(form);
      var val = function (k, fallback) { var v = d.get(k); return v ? String(v) : (fallback || ""); };
      var suggest = val("suggest");
      var sm = suggest.match(/^(\d+)-(\d+)-(\d+)T(\d+):(\d+)/);
      if (sm) {
        var sd = new Date(+sm[1], +sm[2] - 1, +sm[3]), sh = +sm[4];
        suggest = sd.toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long", year: "numeric" }) + " at " + ((sh + 11) % 12 + 1) + ":" + sm[5] + " " + (sh < 12 ? "AM" : "PM") + " (their local time)";
      } else { suggest = suggest.replace("T", " at "); }
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
