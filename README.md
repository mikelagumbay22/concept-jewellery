# Celvaire — fictional fine-jewellery hero concept (Northpage)

Original concept page (fictional brand). Build: `python3 build.py` (src/ → dist/, .nojekyll). Base path /concept-jewellery/.
QA: `python3 qa/bancheck.py dist Celvaire 4`, `python3 qa/audit.py` (axe 390 + 1440), `python3 qa/shots.py http://127.0.0.1:8116/concept-jewellery/ "[data-film]" screenshots 0 0.45 1.0 2`.

Hero: pinned 420vh section; 81 WebP frames (1280×720, 2.1 MB total) drawn on <canvas>, loaded progressively (frame 1, then every 8th/4th/2nd/rest).
Copy fades/un-blurs in at the reveal (opacity/transform/filter only). Mobile/coarse pointer: looping MP4 + Pause. Reduced motion: poster only.

Video (video/): source.mp4 = Seedance 1.5 Pro 8 s 720p (image→video from a GPT Image 2.5 still); the scrub uses 3.0 s → end
(tight on the stone → pull back to the full piece). loop-mobile-720.mp4 = forward+reverse boomerang (10 s, 383 KB, no audio).
All imagery badged "Illustrative AI image/video, concept only".
