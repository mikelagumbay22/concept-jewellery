/* Celvaire concept: scroll-scrubbed WebP frame sequence on <canvas> (desktop), looping MP4 with Pause (mobile), poster only (reduced motion). */
(function () {
  "use strict";
  var root = document.documentElement, film = document.querySelector("[data-film]");
  if (!film) return;
  var N = 81, pad = function (i) { return ("00" + i).slice(-3); };

  if (root.classList.contains("scrub")) {
    var canvas = film.querySelector("canvas"), ctx = canvas.getContext("2d");
    var copyEls = film.querySelectorAll(".film__copy .eyebrow, .film__copy .line, .film__copy .lede, .film__copy .cta");
    var hint = film.querySelector(".film__hint");
    var frames = new Array(N), drawn = -1, ticking = false;
    var load = function (i) {
      if (frames[i]) return;
      var im = new Image(); im.decoding = "async"; im.src = "img/frames/f_" + pad(i + 1) + ".webp";
      frames[i] = im; im.onload = function () { if (drawn === -1 || Math.abs(i - want) < Math.abs(drawn - want)) draw(); };
    };
    // Progressive: first frame, then every 8th, every 4th, every 2nd, then the rest.
    var order = [0];
    [8, 4, 2, 1].forEach(function (s) { for (var i = 0; i < N; i += s) if (order.indexOf(i) < 0) order.push(i); });
    var k = 0, pump = function () { for (var n = 0; n < 6 && k < order.length; n++) load(order[k++]); if (k < order.length) setTimeout(pump, 60); };
    load(0); pump();
    var want = 0;
    var nearest = function (i) { for (var d = 0; d < N; d++) { var a = frames[i - d], b = frames[i + d]; if (a && a.complete && a.naturalWidth) return i - d; if (b && b.complete && b.naturalWidth) return i + d; } return -1; };
    var draw = function () {
      var j = nearest(want); if (j < 0 || j === drawn) return;
      ctx.drawImage(frames[j], 0, 0, canvas.width, canvas.height); drawn = j;
    };
    var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };
    var render = function () {
      ticking = false;
      var r = film.getBoundingClientRect(), span = film.offsetHeight - innerHeight, p = span > 0 ? clamp(-r.top / span) : 1;
      want = Math.round(clamp(p / 0.86) * (N - 1)); draw();
      hint.style.opacity = 1 - clamp(p / 0.08);
      copyEls.forEach(function (el, i) {
        var t = clamp((p - 0.72 - i * 0.035) / 0.12), e = 1 - Math.pow(1 - t, 3);
        el.style.opacity = e;
        el.style.transform = "translateY(" + (28 * (1 - e)) + "px)";
        el.style.filter = "blur(" + (6 * (1 - e)).toFixed(2) + "px)";
      });
    };
    addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(render); } }, { passive: true });
    render();
  }

  if (root.classList.contains("loop")) {
    var v = film.querySelector("video"), btn = film.querySelector("[data-pause]"), lab = film.querySelector("[data-pause-label]");
    var src = v.querySelector("source"); src.src = src.dataset.src; v.load();
    var paused = false, vis = true;
    var sync = function () { if (!paused && vis) v.play().catch(function () {}); else v.pause(); btn.setAttribute("aria-pressed", paused ? "true" : "false"); lab.textContent = paused ? "Play video" : "Pause video"; };
    btn.hidden = false; btn.addEventListener("click", function () { paused = !paused; sync(); });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (e) { vis = e[0].isIntersecting; sync(); }).observe(v);
    sync();
  }
})();
