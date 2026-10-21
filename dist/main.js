/*
 * Domaine Agricole de Néma — mouvements et interactions, sans bibliothèque.
 *
 * Tout est piloté par attributs ; le CSS décide de l'effet. Sans JavaScript, ou quand
 * le visiteur demande moins de mouvement, le contenu est simplement visible.
 *   [data-reveal]        apparaît à son entrée à l'écran (classe .is-in)
 *   [data-words]         titre découpé en mots qui montent l'un après l'autre
 *   [data-count]         nombre qui défile jusqu'à sa valeur
 *   [data-panel]         bande photo qui s'ouvre en cercle (--open de 0 à 1)
 *   [data-draw]          le sillon orange se trace au défilement (--draw de 0 à 1)
 *   [data-slides]        photos qui se succèdent dans le médaillon
 *   [data-preview-list]  aperçu photo qui suit la souris au survol des cultures
 *   [data-gallery]       filtres de la galerie ; a[data-lightbox] ouvre la visionneuse
 *   [data-autoplay]      vidéo muette lue seulement quand elle est visible
 *   [data-magnet]        bouton attiré par la souris
 */
(function () {
  "use strict";

  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!reduce) root.classList.add("motion");

  var clamp = function (v) { return Math.min(1, Math.max(0, v)); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  // --- Menu mobile ------------------------------------------------------------
  var menu = document.getElementById("menu");
  var nav = document.getElementById("nav");
  if (menu && nav) {
    var setMenu = function (open) {
      nav.classList.toggle("open", open);
      root.classList.toggle("menu-open", open);
      menu.setAttribute("aria-expanded", String(open));
      menu.textContent = open ? "Fermer" : "Menu";
    };
    menu.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    $$("a", nav).forEach(function (a) { a.addEventListener("click", function () { setMenu(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
  }

  // --- Titres en mots (garde les <span> et <br> : seuls les nœuds de texte sont découpés) ---
  var wordIndex;
  function splitWords(node) {
    Array.prototype.slice.call(node.childNodes).forEach(function (child) {
      if (child.nodeType === 3) {
        var frag = document.createDocumentFragment();
        child.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
          var outer = document.createElement("span");
          outer.className = "w";
          outer.setAttribute("aria-hidden", "true");
          var inner = document.createElement("span");
          inner.textContent = part;
          inner.style.setProperty("--i", wordIndex++);
          outer.appendChild(inner);
          frag.appendChild(outer);
        });
        child.replaceWith(frag);
      } else if (child.nodeType === 1 && child.tagName !== "BR") {
        splitWords(child);
      }
    });
  }
  $$("[data-words]").forEach(function (el) {
    wordIndex = 0;
    el.setAttribute("aria-label", el.textContent.replace(/\s+/g, " ").trim());
    splitWords(el);
  });

  // --- Compteurs : le nombre défile jusqu'à sa valeur quand il apparaît ------------------
  function countUp(el) {
    var target = Number(el.dataset.count);
    var fmt = function (n) { return el.dataset.raw ? String(n) : n.toLocaleString("fr-FR"); };
    // Une année part d'un siècle plus tôt plutôt que de zéro : le défilement reste lisible.
    var from = el.dataset.raw ? target - 60 : 0;
    var start = performance.now();
    (function tick(now) {
      var t = clamp((now - start) / 1700);
      var eased = 1 - Math.pow(1 - t, 4);
      el.textContent = fmt(Math.round(from + (target - from) * eased));
      if (t < 1) requestAnimationFrame(tick);
    })(start);
  }
  if ("IntersectionObserver" in window && !reduce) {
    var counter = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        countUp(entry.target);
        counter.unobserve(entry.target);
      });
    }, { threshold: 0.6 });
    $$("[data-count]").forEach(function (el) { counter.observe(el); });
  }

  // --- Apparitions -----------------------------------------------------------------
  if ("IntersectionObserver" in window && !reduce) {
    var seen = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        seen.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -6% 0px" });
    // Ce qui est déjà à l'écran au chargement apparaît tout de suite, dans l'ordre de lecture.
    var firstScreen = 0;
    $$("[data-reveal], [data-words]").forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) {
        el.style.transitionDelay = (firstScreen++ * 0.08 + 0.05).toFixed(2) + "s";
        requestAnimationFrame(function () { el.classList.add("is-in"); });
        setTimeout(function () { el.style.transitionDelay = ""; }, 2000);
      } else {
        seen.observe(el);
      }
    });
  } else {
    $$("[data-reveal], [data-words]").forEach(function (el) { el.classList.add("is-in"); });
  }

  // --- Défilement : progression, en-tête, bandes photo, sillon ------------------------------
  var header = document.querySelector(".site-header");
  var panels = $$("[data-panel]");
  var draws = $$("[data-draw]");
  var lastY = window.scrollY;
  var frame = 0;

  function onScroll() {
    frame = 0;
    var y = window.scrollY;
    var vh = window.innerHeight;
    var max = root.scrollHeight - vh;
    root.style.setProperty("--progress", (max > 0 ? y / max : 0).toFixed(4));
    if (header) {
      header.classList.toggle("is-scrolled", y > 8);
      header.classList.toggle("is-hidden", y > 260 && y > lastY && !root.classList.contains("menu-open"));
    }
    lastY = y;
    if (reduce) return;
    panels.forEach(function (panel) {
      var top = panel.getBoundingClientRect().top;
      panel.style.setProperty("--open", clamp((vh - top) / (vh * 0.85)).toFixed(3));
    });
    draws.forEach(function (el) {
      var r = el.getBoundingClientRect();
      el.style.setProperty("--draw", clamp((vh * 0.75 - r.top) / r.height).toFixed(4));
    });
  }
  function requestScroll() { if (!frame) frame = requestAnimationFrame(onScroll); }
  window.addEventListener("scroll", requestScroll, { passive: true });
  window.addEventListener("resize", requestScroll);
  onScroll();

  // --- Médaillon : les photos se succèdent ---------------------------------------------------
  $$("[data-slides]").forEach(function (box) {
    var slides = $$("[data-slide]", box);
    var dots = $$("[data-bar]", box);
    var caption = box.querySelector("[data-caption]");
    var delay = Number(box.dataset.slides) || 5200;
    var current = 0;
    var timer;
    box.style.setProperty("--slide-delay", delay + "ms");
    function show(i) {
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, j) { s.classList.toggle("is-active", j === current); });
      dots.forEach(function (d, j) {
        d.classList.remove("is-active");
        if (j === current) { void d.offsetWidth; d.classList.add("is-active"); }
        d.setAttribute("aria-current", j === current ? "true" : "false");
      });
      if (caption) caption.textContent = slides[current].dataset.label || "";
      clearTimeout(timer);
      if (!reduce && slides.length > 1) timer = setTimeout(function () { show(current + 1); }, delay);
    }
    dots.forEach(function (d, j) { d.addEventListener("click", function () { show(j); }); });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) clearTimeout(timer); else show(current);
    });
    show(0);
  });

  // --- Index des cultures : l'aperçu suit la souris -------------------------------------------
  $$("[data-preview-list]").forEach(function (list) {
    var box = list.closest("section").querySelector("[data-preview-box]");
    if (!box || reduce) return;
    var image = box.querySelector("img");
    var x = 0, y = 0, tx = 0, ty = 0, raf = 0;
    function follow() {
      x += (tx - x) * 0.18;
      y += (ty - y) * 0.18;
      box.style.transform = "translate(" + x.toFixed(1) + "px," + y.toFixed(1) + "px)";
      raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.5 ? requestAnimationFrame(follow) : 0;
    }
    list.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      tx = e.clientX; ty = e.clientY;
      if (!raf) raf = requestAnimationFrame(follow);
    });
    $$("[data-preview]", list).forEach(function (row) {
      row.addEventListener("pointerenter", function (e) {
        if (e.pointerType !== "mouse") return;
        if (!box.classList.contains("is-on")) { x = tx = e.clientX; y = ty = e.clientY; follow(); }
        image.src = row.dataset.preview;
        box.classList.add("is-on");
      });
    });
    list.addEventListener("pointerleave", function () { box.classList.remove("is-on"); });
  });

  // --- Vidéos d'ambiance -------------------------------------------------------------------
  var videos = $$("video[data-autoplay]");
  if (videos.length && "IntersectionObserver" in window) {
    var vio = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        var v = entry.target;
        if (entry.isIntersecting && !reduce) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      });
    }, { threshold: 0.25 });
    videos.forEach(function (v) {
      v.muted = true;
      if (reduce) v.controls = true;
      vio.observe(v);
    });
  }

  // --- Galerie : filtres -------------------------------------------------------------------------
  $$("[data-gallery]").forEach(function (gallery) {
    var items = $$("[data-item]", gallery);
    var filters = $$("[data-filter]", gallery);
    var count = gallery.querySelector("[data-count-label]");
    filters.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = btn.dataset.filter;
        var n = 0;
        filters.forEach(function (b) { b.setAttribute("aria-pressed", String(b === btn)); });
        items.forEach(function (it) {
          var show = f === "all" || it.dataset.item === f;
          it.hidden = !show;
          if (show) n++;
        });
        if (count) count.textContent = n + (n > 1 ? " images" : " image");
      });
    });
  });

  // --- Visionneuse plein écran ----------------------------------------------------------------------
  var box = document.getElementById("lightbox");
  if (box) {
    var img = box.querySelector("[data-lb-img]");
    var cap = box.querySelector("[data-lb-caption]");
    var pos = box.querySelector("[data-lb-count]");
    var list = [];
    var at = 0;
    var render = function () {
      var a = list[at];
      img.src = a.getAttribute("href");
      img.alt = a.dataset.alt || "";
      cap.textContent = a.dataset.caption || "";
      pos.textContent = (at + 1) + " / " + list.length;
    };
    var step = function (d) { at = (at + d + list.length) % list.length; render(); };
    document.addEventListener("click", function (e) {
      var link = e.target.closest("a[data-lightbox]");
      if (!link) return;
      e.preventDefault();
      var group = link.closest("[data-lightbox-group]") || document;
      list = $$("a[data-lightbox]", group).filter(function (a) {
        return !a.closest("[hidden]") && a.getAttribute("aria-hidden") !== "true";
      });
      at = Math.max(0, list.indexOf(link));
      render();
      box.showModal();
    });
    box.querySelector("[data-lb-prev]").addEventListener("click", function () { step(-1); });
    box.querySelector("[data-lb-next]").addEventListener("click", function () { step(1); });
    box.querySelector("[data-lb-close]").addEventListener("click", function () { box.close(); });
    box.addEventListener("click", function (e) { if (e.target === box) box.close(); });
    box.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") step(1);
      if (e.key === "ArrowLeft") step(-1);
    });
    var touchX = null;
    box.addEventListener("touchstart", function (e) { touchX = e.touches[0].clientX; }, { passive: true });
    box.addEventListener("touchend", function (e) {
      if (touchX === null) return;
      var dx = e.changedTouches[0].clientX - touchX;
      if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
      touchX = null;
    });
  }

  // --- Boutons aimantés (souris seulement) ------------------------------------------------------------
  if (!reduce) {
    var magnets = $$("[data-magnet]");
    window.addEventListener("pointermove", function (e) {
      if (e.pointerType !== "mouse") return;
      magnets.forEach(function (m) {
        var r = m.getBoundingClientRect();
        var dx = e.clientX - (r.left + r.width / 2);
        var dy = e.clientY - (r.top + r.height / 2);
        var near = Math.hypot(dx, dy) < Math.max(r.width, r.height) * 0.9;
        m.style.transform = near ? "translate(" + (dx * 0.22).toFixed(1) + "px," + (dy * 0.3).toFixed(1) + "px)" : "";
      });
    }, { passive: true });
  }
})();
