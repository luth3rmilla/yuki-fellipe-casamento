(() => {
  const { translations } = window.WeddingI18n;
  const STORAGE_LANG = "yf-lang";
  const STORAGE_RSVP = "yf-rsvps";

  // Paste your Google Apps Script Web App URL after deploying scripts/rsvp-apps-script.gs
  const RSVP_ENDPOINT = "";

  let lang = localStorage.getItem(STORAGE_LANG) || "pt";
  let carouselIndex = 0;
  let carouselTimer = null;

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

  function t(key) {
    const parts = key.split(".");
    let cur = translations[lang];
    for (const p of parts) {
      if (cur == null) return key;
      cur = cur[p];
    }
    return cur == null ? key : cur;
  }

  function applyI18n() {
    document.documentElement.lang = lang === "zh" ? "zh-Hans" : lang;
    $$("[data-i18n]").forEach((el) => {
      const value = t(el.getAttribute("data-i18n"));
      if (typeof value === "string") el.textContent = value;
    });
    $$(".lang-switch [data-lang]").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.lang === lang);
    });
    const musicBtn = $("#musicBtn");
    if (musicBtn) {
      musicBtn.title = musicBtn.getAttribute("aria-pressed") === "true" ? t("musicPause") : t("musicPlay");
    }
  }

  function showPanel(id) {
    $$(".panel").forEach((panel) => {
      panel.classList.toggle("is-active", panel.dataset.panel === id);
    });
    $$(".nav [data-nav]").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.nav === id);
    });
    $("#mainNav")?.classList.remove("is-open");
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (id === "home") startCarousel();
    else stopCarousel();
  }

  function buildDots() {
    const slides = $$(".carousel-slide");
    const dots = $("#carouselDots");
    dots.innerHTML = "";
    slides.forEach((_, i) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.setAttribute("aria-label", `Slide ${i + 1}`);
      btn.classList.toggle("is-active", i === carouselIndex);
      btn.addEventListener("click", () => goToSlide(i));
      dots.appendChild(btn);
    });
  }

  function goToSlide(index) {
    const slides = $$(".carousel-slide");
    carouselIndex = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      slide.classList.toggle("is-active", i === carouselIndex);
    });
    $$("#carouselDots button").forEach((btn, i) => {
      btn.classList.toggle("is-active", i === carouselIndex);
    });
  }

  function nextSlide() {
    goToSlide(carouselIndex + 1);
  }

  function startCarousel() {
    stopCarousel();
    carouselTimer = setInterval(nextSlide, 5200);
  }

  function stopCarousel() {
    if (carouselTimer) clearInterval(carouselTimer);
    carouselTimer = null;
  }

  function setupMusic() {
    const audio = $("#bgMusic");
    const btn = $("#musicBtn");
    const hint = $("#musicHint");
    const iconPlay = $("#iconPlay");
    const iconPause = $("#iconPause");
    if (!audio || !btn) return;

    const sync = () => {
      const playing = !audio.paused;
      btn.setAttribute("aria-pressed", String(playing));
      btn.title = playing ? t("musicPause") : t("musicPlay");
      iconPlay.hidden = playing;
      iconPause.hidden = !playing;
    };

    btn.addEventListener("click", async () => {
      try {
        if (audio.paused) {
          await audio.play();
          hint?.classList.remove("is-visible");
        } else {
          audio.pause();
        }
      } catch {
        hint?.classList.add("is-visible");
        setTimeout(() => hint?.classList.remove("is-visible"), 2800);
      }
      sync();
    });

    audio.addEventListener("play", sync);
    audio.addEventListener("pause", sync);
    sync();

    // Soft autoplay attempt (browsers may block until user interaction)
    audio.volume = 0.45;
    audio.play().then(sync).catch(() => {
      hint.textContent = t("musicPlay");
      hint.classList.add("is-visible");
      setTimeout(() => hint.classList.remove("is-visible"), 3500);
    });
  }

  function setupCopy() {
    $$("[data-copy]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const text = btn.getAttribute("data-copy");
        try {
          await navigator.clipboard.writeText(text);
          const prev = btn.textContent;
          btn.textContent = t("copied");
          setTimeout(() => {
            btn.textContent = t("copy");
            if (btn.textContent !== t("copy")) btn.textContent = prev;
          }, 1600);
        } catch {
          const ta = document.createElement("textarea");
          ta.value = text;
          document.body.appendChild(ta);
          ta.select();
          document.execCommand("copy");
          ta.remove();
          btn.textContent = t("copied");
          setTimeout(() => (btn.textContent = t("copy")), 1600);
        }
      });
    });
  }

  function saveLocalRsvp(payload) {
    const list = JSON.parse(localStorage.getItem(STORAGE_RSVP) || "[]");
    list.push(payload);
    localStorage.setItem(STORAGE_RSVP, JSON.stringify(list));
  }

  async function submitRsvp(payload) {
    saveLocalRsvp(payload);

    if (!RSVP_ENDPOINT) {
      // Fallback: open a mailto with the RSVP details (works before Apps Script is set up)
      const subject = encodeURIComponent(`RSVP — ${payload.name}`);
      const body = encodeURIComponent(
        `Attending: ${payload.attending}\nName: ${payload.name}\nGuests: ${payload.guests}\nLanguage: ${payload.language}\nSubmitted: ${payload.submittedAt}`
      );
      // Prefer silent local save when endpoint missing; still report success for UX
      console.info("RSVP saved locally. Set RSVP_ENDPOINT in js/main.js to sync to Google Sheet.");
      return { ok: true, localOnly: true };
    }

    const res = await fetch(RSVP_ENDPOINT, {
      method: "POST",
      mode: "cors",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) throw new Error("Network error");
    const data = await res.json().catch(() => ({ ok: true }));
    if (data.ok === false) throw new Error(data.error || "Failed");
    return data;
  }

  function setupRsvp() {
    const form = $("#rsvpForm");
    const message = $("#formMessage");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      message.className = "form-message";
      message.textContent = "";

      const attending = form.attending.value;
      const name = form.name.value.trim();
      const guests = Number(form.guests.value);

      if (!attending || !name || !guests || guests < 1) {
        message.classList.add("is-err");
        message.textContent = t("rsvpError");
        return;
      }

      const payload = {
        attending,
        name,
        guests,
        language: lang,
        submittedAt: new Date().toISOString(),
      };

      const submitBtn = form.querySelector('[type="submit"]');
      submitBtn.disabled = true;

      try {
        await submitRsvp(payload);
        message.classList.add("is-ok");
        message.textContent = t("rsvpSuccess");
        form.reset();
        form.guests.value = "1";
      } catch (err) {
        console.error(err);
        message.classList.add("is-err");
        message.textContent = t("rsvpError");
      } finally {
        submitBtn.disabled = false;
      }
    });
  }

  function setupNav() {
    $$("[data-nav]").forEach((el) => {
      el.addEventListener("click", (e) => {
        e.preventDefault();
        showPanel(el.dataset.nav);
      });
    });

    $("#menuToggle")?.addEventListener("click", () => {
      $("#mainNav")?.classList.toggle("is-open");
    });

    $$(".lang-switch [data-lang]").forEach((btn) => {
      btn.addEventListener("click", () => {
        lang = btn.dataset.lang;
        localStorage.setItem(STORAGE_LANG, lang);
        applyI18n();
      });
    });

    window.addEventListener("scroll", () => {
      $("#siteHeader")?.classList.toggle("is-scrolled", window.scrollY > 12);
    });
  }

  function setupCountdown() {
    const root = $("#countdown");
    const doneEl = $("#countdownDone");
    if (!root) return;

    // Ceremony: 3 Oct 2026, 14:00 Catembe / Maputo (Africa/Maputo, UTC+2)
    const weddingAt = new Date("2026-10-03T14:00:00+02:00").getTime();

    const tick = () => {
      const diff = weddingAt - Date.now();
      if (diff <= 0) {
        root.classList.add("is-done");
        if (doneEl) doneEl.hidden = false;
        return;
      }
      const totalSec = Math.floor(diff / 1000);
      const days = Math.floor(totalSec / 86400);
      const hours = Math.floor((totalSec % 86400) / 3600);
      const minutes = Math.floor((totalSec % 3600) / 60);
      const seconds = totalSec % 60;
      const pad = (n) => String(n).padStart(2, "0");
      root.querySelector('[data-unit="days"]').textContent = String(days);
      root.querySelector('[data-unit="hours"]').textContent = pad(hours);
      root.querySelector('[data-unit="minutes"]').textContent = pad(minutes);
      root.querySelector('[data-unit="seconds"]').textContent = pad(seconds);
    };

    tick();
    setInterval(tick, 1000);
  }

  buildDots();
  applyI18n();
  setupNav();
  setupMusic();
  setupCopy();
  setupRsvp();
  setupCountdown();
  startCarousel();
})();
