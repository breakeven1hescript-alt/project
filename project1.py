<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Multi-Axis Spacetime Fabric — Lucky Model v68</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  html, body { width: 100%; height: 100%; overflow: hidden; background: #ffffff; font-family: "Segoe UI", system-ui, -apple-system, sans-serif; }
  canvas { display: block; touch-action: none; }

  /* ---------- loading overlay ---------- */
  #overlay { position: fixed; inset: 0; z-index: 100; display: flex; flex-direction: column; align-items: center; justify-content: center;
    background: radial-gradient(circle at 50% 40%, #ffffff, #eaf1fb); color: #123; text-align: center; }
  #overlay .spinner { width: 46px; height: 46px; border-radius: 50%; border: 4px solid rgba(18, 60, 120, .15); border-top-color: #12d98c;
    animation: spin 1s linear infinite; margin-bottom: 18px; }
  @keyframes spin { to { transform: rotate(360deg); } }
  #overlay h1 { font-size: 19px; font-weight: 600; letter-spacing: .4px; }
  #overlay p { margin-top: 8px; font-size: 13px; color: #4a5a70; max-width: 460px; line-height: 1.5; }
  #overlay .err { color: #d33; font-weight: 600; }

  /* ---------- control panel ---------- */
  #panel { position: fixed; top: 14px; left: 14px; width: 336px; max-height: calc(100vh - 40px); overflow-y: auto; z-index: 10;
    background: rgba(9, 14, 26, .84); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,.13); border-radius: 14px; color: #dfe8f7; font-size: 12.5px;
    box-shadow: 0 10px 34px rgba(8, 16, 36, .35); padding: 12px 13px 8px; user-select: none; }
  #panel::-webkit-scrollbar { width: 8px; } #panel::-webkit-scrollbar-thumb { background: rgba(255,255,255,.18); border-radius: 4px; }
  #panel .head { display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 10px; }
  #panel .head h2 { font-size: 13.5px; font-weight: 700; letter-spacing: .3px; }
  #panel .head h2 i { color: #2fe8a0; font-style: normal; }
  #panel .head span { font-size: 10px; color: #8ea3c4; letter-spacing: 1.2px; }

  .section { border-top: 1px solid rgba(255,255,255,.08); padding-top: 8px; margin-top: 8px; }
  .section > .ttl { font-size: 10px; font-weight: 700; letter-spacing: 1.6px; color: #7f93b6; margin-bottom: 6px; text-transform: uppercase; }
  .btnrow { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .btn { cursor: pointer; border-radius: 8px; padding: 7px 6px; font-size: 11.5px; font-weight: 600; color: #fff; border: 1px solid rgba(255,255,255,.22);
    background: rgba(255,255,255,.06); transition: filter .15s, transform .05s; text-align: center; }
  .btn:hover { filter: brightness(1.18); } .btn:active { transform: scale(.97); }
  .btn:disabled { opacity: .35; cursor: default; filter: none; }
  .btn.sun { box-shadow: inset 0 0 0 1px rgba(255,190,80,.55); color: #ffd98a; }
  .btn.bh  { box-shadow: inset 0 0 0 1px rgba(255,120,90,.5); color: #ffb0a0; }
  .btn.ns  { box-shadow: inset 0 0 0 1px rgba(130,190,255,.5); color: #a8d2ff; }
  .btn.ps  { box-shadow: inset 0 0 0 1px rgba(190,120,255,.55); color: #d8b8ff; }
  .btn.met { box-shadow: inset 0 0 0 1px rgba(255,160,110,.45); color: #ffc9a0; }
  .btn.lgt { box-shadow: inset 0 0 0 1px rgba(255,90,120,.5); color: #ffb3c0; }
  .btn.star { box-shadow: inset 0 0 0 1px rgba(255,230,140,.6); color: #ffe9a8; }
  .btn.wide { grid-column: 1 / -1; }

  .objrow { display: flex; align-items: center; gap: 7px; padding: 5px 6px; border-radius: 7px; margin-bottom: 4px; background: rgba(255,255,255,.045); }
  .objrow.sel { outline: 1px solid #2fe8a0; }
  .objrow .nm { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 11.5px; }
  .objrow .nm small { color: #7f93b6; font-size: 10px; }
  .objrow .rm { cursor: pointer; color: #ff8f9e; border: none; background: none; font-size: 13px; padding: 0 3px; }
  .objrow .rm:hover { color: #ff5a70; }
  #selCard { margin-top: 6px; padding: 8px; border-radius: 8px; background: rgba(47,232,160,.09); border: 1px solid rgba(47,232,160,.35); font-size: 11.5px; }
  #selCard .lbl { color: #8fd8b8; font-size: 10px; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px; }
  #selCard .mono { font-family: Consolas, monospace; color: #cfe9de; font-size: 10.5px; }
  #selCard label { display: block; margin-top: 6px; color: #9fb8d6; font-size: 10.5px; }
  #selCard input[type=range] { width: 100%; }

  details.section summary { cursor: pointer; font-size: 10px; font-weight: 700; letter-spacing: 1.6px; color: #7f93b6; text-transform: uppercase;
    list-style: none; display: flex; align-items: center; gap: 6px; }
  details.section summary::before { content: "▸"; transition: transform .15s; color: #5d7194; }
  details.section[open] summary::before { transform: rotate(90deg); }
  details.section[open] { border-top: 1px solid rgba(255,255,255,.08); padding-top: 8px; margin-top: 8px; }
  details.section { border-top: 1px solid rgba(255,255,255,.08); padding-top: 8px; margin-top: 8px; }

  .slider { margin: 7px 0; }
  .slider .row { display: flex; justify-content: space-between; font-size: 11px; color: #b9c8e2; margin-bottom: 2px; }
  .slider .row .val { color: #2fe8a0; font-family: Consolas, monospace; }
  input[type=range] { -webkit-appearance: none; width: 100%; height: 4px; border-radius: 3px; background: rgba(255,255,255,.16); outline: none; }
  input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 13px; height: 13px; border-radius: 50%;
    background: #2fe8a0; border: 2px solid #0c1424; cursor: pointer; }
  input[type=checkbox] { accent-color: #2fe8a0; }
  select { background: rgba(255,255,255,.08); color: #dfe8f7; border: 1px solid rgba(255,255,255,.2); border-radius: 6px; padding: 4px 6px; font-size: 11px; }

  .seg { display: flex; gap: 4px; }
  #viewSeg { flex-wrap: wrap; }
  #viewSeg .segbtn { flex: 1 1 45%; }
  .seg .segbtn { flex: 1; cursor: pointer; text-align: center; padding: 5px 4px; font-size: 10.5px; border-radius: 6px;
    background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.14); color: #9fb3d0; }
  .seg .segbtn.on { background: rgba(47,232,160,.18); border-color: rgba(47,232,160,.6); color: #2fe8a0; font-weight: 700; }

  #readout { font-family: Consolas, "SF Mono", monospace; font-size: 10.5px; line-height: 1.65; color: #a9c3ea; white-space: pre; }
  #readout b { color: #2fe8a0; font-weight: 600; }

  /* ---------- hints / banners ---------- */
  #hint { position: fixed; bottom: 12px; left: 50%; transform: translateX(-50%); z-index: 10; padding: 7px 16px; border-radius: 999px;
    background: rgba(9,14,26,.72); color: #c9d6ee; font-size: 11px; letter-spacing: .2px; backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,.12); white-space: nowrap; }
  #banner { position: fixed; top: 16px; left: 50%; transform: translateX(-50%); z-index: 20; padding: 9px 18px; border-radius: 10px;
    background: rgba(255, 61, 92, .92); color: #fff; font-size: 12.5px; font-weight: 600; box-shadow: 0 8px 26px rgba(255,61,92,.35);
    display: none; }
  #banner code { background: rgba(255,255,255,.22); padding: 1px 5px; border-radius: 4px; font-size: 11px; }

  /* ---------- details / inspector panel ---------- */
  #details { position: fixed; top: 14px; right: 14px; width: 340px; max-height: calc(100vh - 40px); overflow-y: auto; z-index: 10;
    background: rgba(9, 14, 26, .88); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(47,232,160,.25); border-radius: 14px; color: #dfe8f7; font-size: 12px;
    box-shadow: 0 10px 34px rgba(8, 16, 36, .45); padding: 14px; user-select: none;
    transition: opacity .25s, transform .25s; }
  #details.hidden { opacity: 0; transform: translateX(20px); pointer-events: none; }
  #details::-webkit-scrollbar { width: 7px; } #details::-webkit-scrollbar-thumb { background: rgba(255,255,255,.15); border-radius: 4px; }
  #details .dHead { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
  #details .dHead h3 { font-size: 14px; font-weight: 700; color: #2fe8a0; margin: 0; }
  #details .dHead .close { cursor: pointer; color: #ff8f9e; font-size: 16px; padding: 0 4px; background: none; border: none; }
  #details .dHead .close:hover { color: #ff5a70; }
  #details .dCat { font-size: 9.5px; font-weight: 700; letter-spacing: 1.4px; color: #7f93b6; text-transform: uppercase;
    margin-top: 10px; margin-bottom: 4px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,.08); }
  #details .dCat:first-child { border-top: none; padding-top: 0; margin-top: 6px; }
  #details .dRow { display: flex; justify-content: space-between; padding: 2px 0; font-size: 11.5px; }
  #details .dRow .dLbl { color: #8ea3c4; }
  #details .dRow .dVal { color: #2fe8a0; font-family: Consolas, monospace; font-size: 11px; }
  #details .dEq { font-family: Consolas, monospace; font-size: 10.5px; color: #c9ddf0; background: rgba(255,255,255,.05);
    border-radius: 6px; padding: 6px 8px; margin: 5px 0; line-height: 1.6; white-space: pre-wrap; word-break: break-word; }
  #details .dTxt { font-size: 11.5px; color: #b9c8e2; line-height: 1.55; margin: 3px 0; }
  #details .dTxt i { color: #8fd8b8; font-style: normal; }

  #fps { position: fixed; top: 14px; right: 14px; z-index: 10; font-family: Consolas, monospace; font-size: 11px; color: #28406a;
    background: rgba(255,255,255,.7); padding: 4px 9px; border-radius: 8px; border: 1px solid rgba(30,60,110,.15); }
  /* ---------- cover page (Techsense master screen) ---------- */
  #overlay { display: none; }   /* deferred boot: #overlay is the loader only after the cover CTA */
  #coverPage { --gold: #d4af37; --goldSoft: #e8c988;
    position: fixed; inset: 0; z-index: 1000; overflow: hidden; color: #dfe8f7;
    font-family: "Inter", "Segoe UI", system-ui, sans-serif; -webkit-font-smoothing: antialiased;
    background: radial-gradient(1400px 950px at 80% 8%, #131d33 0%, #0a0f1d 48%, #05070d 100%);
    transition: opacity .65s cubic-bezier(.45,0,.2,1), transform .65s cubic-bezier(.45,0,.2,1); }
  #coverPage.leaving { opacity: 0; transform: scale(1.03); pointer-events: none; }
  /* faint fabric-grid motif, radially masked so it melts into the dark */
  #coverPage::before { content: ""; position: absolute; inset: 0; z-index: 0; pointer-events: none;
    background-image: repeating-linear-gradient(0deg, rgba(150,170,215,.05) 0 1px, transparent 1px 46px),
                      repeating-linear-gradient(90deg, rgba(150,170,215,.05) 0 1px, transparent 1px 46px);
    -webkit-mask-image: radial-gradient(ellipse 80% 72% at 50% 44%, #000 20%, transparent 80%);
    mask-image: radial-gradient(ellipse 80% 72% at 50% 44%, #000 20%, transparent 80%); }
  #coverStars { position: absolute; inset: 0; z-index: 0; width: 100%; height: 100%; }
  #coverPage .cvScroll { position: relative; z-index: 2; height: 100%; overflow-y: auto; overflow-x: hidden;
    -webkit-overflow-scrolling: touch; }
  #coverPage .cvScroll::-webkit-scrollbar { width: 8px; }
  #coverPage .cvScroll::-webkit-scrollbar-thumb { background: rgba(212,175,55,.25); border-radius: 4px; }
  .cvWrap { max-width: 1060px; margin: 0 auto; display: flex; flex-direction: column; align-items: center;
    text-align: center; padding: clamp(22px, 5.5vh, 56px) clamp(20px, 5vw, 64px) clamp(20px, 4.5vh, 44px); }
  .cvTitle { font-family: "Cormorant Garamond", Georgia, "Times New Roman", serif; text-transform: uppercase;
    font-weight: 600; color: #f1f4fb; user-select: none; }
  .cvTitle .a { display: block; font-size: clamp(10.5px, 1.25vw, 14px); font-weight: 600;
    letter-spacing: .5em; text-indent: .5em; color: var(--goldSoft); margin-bottom: clamp(8px, 1.5vh, 16px); }
  .cvTitle .b { display: block; font-size: clamp(1.7rem, 5.7vw, 4.6rem); line-height: 1.05;
    letter-spacing: .09em; text-indent: .09em; }
  .cvRule { height: 1px; width: clamp(88px, 18vw, 210px); margin-top: clamp(12px, 2.2vh, 22px); opacity: .9;
    background: linear-gradient(90deg, transparent, var(--gold) 20%, var(--gold) 80%, transparent); }
  .cvSub { font-family: "Cormorant Garamond", Georgia, serif; font-style: italic; font-weight: 500;
    font-size: clamp(1rem, 1.7vw, 1.26rem); color: #aebbd2; margin-top: clamp(10px, 1.9vh, 18px); }
  .cvLead { max-width: 700px; margin: clamp(16px, 3.4vh, 34px) auto 0; font-size: clamp(13.5px, 1.35vw, 15.5px);
    line-height: 1.85; color: #c9d4e6; }
  .cvLead strong { color: #f0f3fb; font-weight: 600; }
  .cvFeats { width: 100%; max-width: 1000px; margin: clamp(18px, 3.8vh, 38px) auto 0;
    display: grid; grid-template-columns: repeat(3, 1fr); gap: clamp(10px, 1.9vw, 24px); text-align: left; }
  .cvFeat { border: 1px solid rgba(255,255,255,.09); border-radius: 14px; background: rgba(255,255,255,.03);
    padding: clamp(18px, 2.6vw, 26px) clamp(16px, 2.2vw, 24px); }
  .cvIcon { width: 30px; height: 30px; color: var(--gold); opacity: .95; margin-bottom: 13px; }
  .cvFeat h3 { font-size: 10.5px; font-weight: 600; letter-spacing: .18em; text-transform: uppercase;
    color: var(--goldSoft); margin-bottom: 9px; line-height: 1.6; }
  .cvFeat p { font-size: 12.5px; line-height: 1.72; color: #9dacc6; }
  .cvNote { max-width: 680px; margin: clamp(14px, 2.8vh, 28px) auto 0; font-size: 12.5px; line-height: 1.8; color: #8fa0bd; }
  .cvNote i { color: #b9c6dd; }
  .cvCta { margin-top: clamp(18px, 3.6vh, 36px); display: flex; flex-direction: column; align-items: center; gap: 13px; }
  .cvBtn { cursor: pointer; font-family: "Inter", "Segoe UI", sans-serif; font-size: 12px; font-weight: 600;
    letter-spacing: .3em; text-indent: .3em; text-transform: uppercase; color: #eedba2;
    background: linear-gradient(180deg, rgba(212,175,55,.16), rgba(212,175,55,.05));
    border: 1px solid rgba(212,175,55,.55); border-radius: 999px; padding: 15px 40px 14px;
    transition: filter .18s, transform .12s, box-shadow .25s, border-color .25s;
    box-shadow: 0 14px 30px rgba(0,0,0,.25); }
  .cvBtn:hover { filter: brightness(1.15); transform: translateY(-1px);
    border-color: rgba(232,201,136,.85); box-shadow: 0 0 28px rgba(212,175,55,.26), 0 18px 34px rgba(0,0,0,.3); }
  .cvBtn:active { transform: scale(.97); filter: brightness(1.05); }
  .cvPill { display: inline-flex; align-items: center; gap: 7px; font-size: 9px; font-weight: 600;
    letter-spacing: .24em; text-transform: uppercase; color: #8ea0bd;
    border: 1px solid rgba(255,255,255,.13); border-radius: 999px; padding: 6px 13px 5px;
    background: rgba(255,255,255,.03); }
  .cvPill i { width: 5px; height: 5px; border-radius: 50%; background: var(--gold);
    box-shadow: 0 0 8px var(--gold); }
  .cvFoot { margin-top: clamp(12px, 2.4vh, 24px); font-size: 9.5px; letter-spacing: .22em;
    text-transform: uppercase; color: #5d6d8b; }
  @media (max-width: 760px) {
    .cvFeats { grid-template-columns: 1fr; max-width: 470px; }
    .cvTitle .b { font-size: clamp(1.42rem, 8.2vw, 2.6rem); letter-spacing: .06em; text-indent: .06em; }
  }
  @media (prefers-reduced-motion: reduce) {
    #coverPage { transition-duration: .25s; }
  }

  /* tiny "upcoming" pill on the 5D view tab — preview framing, tab stays live */
  #viewSeg .segbtn .upTag { display: inline-block; margin-left: 5px; font-size: 6.5px; font-weight: 700;
    letter-spacing: .12em; vertical-align: 2px; color: #c9b072;
    background: rgba(212,175,55,.13); border: 1px solid rgba(212,175,55,.4);
    border-radius: 999px; padding: 1px 5px 1px 6px; text-transform: uppercase; }

  /* ================================================================== */
  /* Cover v2 theme — black / gold / white, space backdrop, scroll show  */
  /* ================================================================== */
  #coverPage.coverV2 { background-color: #020204;
    background-image:
      radial-gradient(1300px 900px at 50% -12%, rgba(212,175,55,.09), transparent 62%),
      radial-gradient(950px 700px at 92% 108%, rgba(255,255,255,.05), transparent 60%),
      radial-gradient(1000px 760px at 4% 104%, rgba(212,175,55,.04), transparent 55%);
    color: #fff; }
  #coverPage.coverV2::before { background-image:
      repeating-linear-gradient(0deg, rgba(212,175,55,.032) 0 1px, transparent 1px 52px),
      repeating-linear-gradient(90deg, rgba(212,175,55,.032) 0 1px, transparent 1px 52px);
    opacity: .5;
    -webkit-mask-image: radial-gradient(ellipse 95% 85% at 50% 32%, #000 12%, transparent 76%);
    mask-image: radial-gradient(ellipse 95% 85% at 50% 32%, #000 12%, transparent 76%); }
  /* soft vignette above the space canvas, below the text */
  #coverPage.coverV2::after { content: ""; position: absolute; inset: 0; z-index: 1; pointer-events: none;
    background: radial-gradient(ellipse 125% 105% at 50% 42%, transparent 55%, rgba(0,0,0,.6) 100%); }
  #coverPage.coverV2 .cvScroll { z-index: 3; }

  /* --- layout: hero first, then scrollable acts, via flex order --- */
  #coverPage.coverV2 .cvWrap { max-width: 1140px; display: flex; flex-direction: column;
    align-items: center; text-align: center; gap: clamp(40px, 7vh, 78px);
    padding-top: clamp(64px, 11vh, 118px); }
  #coverPage.coverV2 .cvWrap > .cvHead  { order: 10; width: 100%; }
  #coverPage.coverV2 .cvWrap > .cvLead  { order: 20; margin: 0; max-width: 780px; text-align: center; }
  #coverPage.coverV2 .cvWrap > .cvCta   { order: 30; margin: 0; }
  #coverPage.coverV2 .cvWrap > .cvCue   { order: 34; }
  #coverPage.coverV2 .cvWrap > #cvWhat  { order: 50; }
  #coverPage.coverV2 .cvWrap > .cvFeats { order: 60; margin: 0; max-width: 100%; }
  #coverPage.coverV2 .cvWrap > .cvNote  { order: 61; display: none; }
  #coverPage.coverV2 .cvWrap > .cvControls { order: 70; }
  #coverPage.coverV2 .cvWrap > .cvOutro { order: 80; margin: 0; }
  #coverPage.coverV2 .cvWrap > .cvFoot  { order: 90; margin: 0; }

  /* --- hero typography --- */
  #coverPage.coverV2 .cvTitle { color: #fff; text-shadow: 0 0 46px rgba(212,175,55,.28); }
  #coverPage.coverV2 .cvTitle .a { color: transparent;
    background: linear-gradient(100deg, #a8852f 0%, #e8c988 25%, #fff6d8 50%, #e8c988 75%, #a8852f 100%);
    background-size: 220% 100%; -webkit-background-clip: text; background-clip: text;
    animation: cvShimmer 7s linear infinite; text-shadow: none; }
  #coverPage.coverV2 .cvTitle .b { color: #fff; }
  #coverPage.coverV2 .cvRule { background: linear-gradient(90deg, transparent, #d4af37 18%, #f6e7b6 50%, #d4af37 82%, transparent);
    box-shadow: 0 0 18px rgba(212,175,55,.45); }
  #coverPage.coverV2 .cvSub { color: #e3dcc8; }
  #coverPage.coverV2 .cvLead { color: #e9e4d8; font-family: "Cormorant Garamond", Georgia, serif;
    font-weight: 500; font-size: clamp(1.08rem, 1.65vw, 1.36rem); line-height: 1.7; letter-spacing: .012em; }
  #coverPage.coverV2 .cvLead strong { color: #fff; font-weight: 700; }
  #coverPage.coverV2 .cvLead em { color: #e6cf96; font-style: italic; }
  #coverPage.coverV2 .cvWrap > .cvBasis { order: 21; margin: 0; max-width: 780px; text-align: center;
    font-family: "Cormorant Garamond", Georgia, serif; font-style: italic; font-weight: 500;
    font-size: clamp(1rem, 1.5vw, 1.24rem); line-height: 1.65; color: #d8cdb2; }
  #coverPage.coverV2 .cvBasis b { color: #fff; font-weight: 700; }
  #coverPage.coverV2 .cvBasis .fx { color: #e0c98f; white-space: nowrap; }

  /* --- CTA (both hero + outro) --- */
  #coverPage.coverV2 .cvBtn { position: relative; overflow: hidden;
    background: rgba(2,2,6,.6); border: 1px solid rgba(212,175,55,.85); color: #f7ecc2;
    padding: 17px 48px 16px; letter-spacing: .32em; text-indent: .32em;
    box-shadow: 0 18px 44px rgba(0,0,0,.5), inset 0 0 24px rgba(212,175,55,.08);
    animation: cvGlow 3.6s ease-in-out infinite; }
  #coverPage.coverV2 .cvBtn::after { content: ""; position: absolute; top: 0; left: -90%; width: 55%; height: 100%;
    background: linear-gradient(100deg, transparent, rgba(255,255,255,.32), transparent);
    transform: skewX(-20deg); transition: left .55s ease; }
  #coverPage.coverV2 .cvBtn:hover { animation-play-state: paused; filter: brightness(1.18); }
  #coverPage.coverV2 .cvBtn:hover::after { left: 140%; }
  #coverPage.coverV2 .cvPill { color: #cfc4a4; border-color: rgba(212,175,55,.28); background: rgba(212,175,55,.05); }
  #coverPage.coverV2 .cvPill i { box-shadow: 0 0 10px #d4af37; }

  /* --- section scaffolding (scrollable acts) --- */
  #coverPage.coverV2 .cvSec, #coverPage.coverV2 .cvOutro { width: 100%; text-align: left; }
  #coverPage.coverV2 .cvSecHead { margin-bottom: clamp(20px, 3vh, 30px); }
  #coverPage.coverV2 .cvSecKicker { display: flex; align-items: center; gap: 16px;
    font-size: 10px; font-weight: 600; letter-spacing: .5em; text-indent: .02em; text-transform: uppercase;
    color: #d4af37; opacity: .95; }
  #coverPage.coverV2 .cvSecKicker::after { content: ""; height: 1px; width: clamp(60px, 10vw, 140px);
    background: linear-gradient(90deg, rgba(212,175,55,.7), transparent); }
  #coverPage.coverV2 .cvSecTitle { font-family: "Cormorant Garamond", Georgia, serif; font-weight: 600;
    font-size: clamp(1.75rem, 3.4vw, 2.7rem); color: #fff; letter-spacing: .02em;
    text-transform: uppercase; line-height: 1.1; margin-top: 12px; }
  #coverPage.coverV2 .cvSecRule { height: 1px; width: 130px; margin-top: 16px;
    background: linear-gradient(90deg, rgba(212,175,55,.9), rgba(212,175,55,.05));
    box-shadow: 0 0 14px rgba(212,175,55,.35); }

  /* --- "what's inside" cards --- */
  #coverPage.coverV2 .cvWhat { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; width: 100%; }
  #coverPage.coverV2 .cvWhatCard { display: flex; align-items: flex-start; gap: 18px;
    border: 1px solid rgba(212,175,55,.2); border-radius: 16px; padding: 20px 22px;
    background: linear-gradient(160deg, rgba(212,175,55,.07), rgba(255,255,255,.02));
    transition: transform .35s ease, border-color .35s ease, box-shadow .35s ease, background .35s ease; }
  #coverPage.coverV2 .cvWhatCard:hover { transform: translateY(-5px);
    border-color: rgba(232,201,136,.8); background: linear-gradient(160deg, rgba(212,175,55,.13), rgba(255,255,255,.04));
    box-shadow: 0 16px 38px rgba(0,0,0,.5), 0 0 30px rgba(212,175,55,.13); }
  #coverPage.coverV2 .cvWhatCard:nth-child(5) { grid-column: 1 / -1; }
  #coverPage.coverV2 .cvNum { font-family: "Cormorant Garamond", Georgia, serif; font-size: 34px; font-weight: 600;
    line-height: .9; color: #d4af37; text-shadow: 0 0 20px rgba(212,175,55,.5); }
  #coverPage.coverV2 .cvWhatCard h3 { font-size: 12.5px; font-weight: 600; letter-spacing: .18em;
    text-transform: uppercase; color: #f6edd0; margin: 2px 0 8px; }
  #coverPage.coverV2 .cvWhatCard p { font-size: 13px; line-height: 1.72; color: #d4cdbc; }

  /* --- pillars (three ways of seeing) --- */
  #coverPage.coverV2 .cvFeats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; text-align: left; }
  #coverPage.coverV2 .cvFeat { background: rgba(255,255,255,.02); border-color: rgba(212,175,55,.22);
    transition: transform .35s ease, border-color .35s ease, box-shadow .35s ease, background .35s ease; }
  #coverPage.coverV2 .cvFeat:hover { transform: translateY(-6px); border-color: rgba(232,201,136,.85);
    box-shadow: 0 18px 42px rgba(0,0,0,.52), 0 0 34px rgba(212,175,55,.15);
    background: rgba(255,255,255,.035); }
  #coverPage.coverV2 .cvFeat h3 { color: #ecd9a2; }
  #coverPage.coverV2 .cvFeat p { color: #cfc8b6; }
  #coverPage.coverV2 .cvIcon { filter: drop-shadow(0 0 9px rgba(212,175,55,.6)); }
  #coverPage.coverV2 .cvFeat:hover .cvIcon { filter: drop-shadow(0 0 14px rgba(232,201,136,.9)); }

  /* --- flight manual --- */
  #coverPage.coverV2 .cvKeys { list-style: none; display: flex; flex-wrap: wrap; gap: 10px; }
  #coverPage.coverV2 .cvKeys li { display: flex; align-items: center; gap: 10px;
    border: 1px solid rgba(255,255,255,.13); background: rgba(255,255,255,.03);
    border-radius: 10px; padding: 8px 14px; font-size: 12px; color: #cfc8b6; }
  #coverPage.coverV2 .cvKeys b { font-family: Consolas, "SF Mono", monospace; font-size: 10.5px;
    color: #ecd9a2; background: rgba(212,175,55,.12); border: 1px solid rgba(212,175,55,.4);
    border-radius: 6px; padding: 2px 8px; letter-spacing: .08em; }
  #coverPage.coverV2 .cvKeys li span { letter-spacing: .06em; text-transform: uppercase; font-size: 10px; }

  /* --- outro --- */
  #coverPage.coverV2 .cvOutro { display: flex; flex-direction: column; align-items: center; text-align: center;
    padding: clamp(30px, 6vh, 54px) 0 clamp(6px, 1vh, 10px); }
  #coverPage.coverV2 .cvOutroLine { font-family: "Cormorant Garamond", Georgia, serif; font-style: italic;
    font-size: clamp(1.65rem, 3.4vw, 2.8rem); color: #fff; margin-bottom: 32px;
    text-shadow: 0 0 34px rgba(212,175,55,.25); }
  #coverPage.coverV2 .cvOutroLine i { color: #ecd9a2; }
  #coverPage.coverV2 .cvFoot { color: #8a7f64; letter-spacing: .26em; }

  /* --- scroll cue --- */
  #coverPage.coverV2 .cvCue { display: inline-flex; flex-direction: column; align-items: center; gap: 4px;
    cursor: pointer; color: #b3a88a; font-size: 9.5px; letter-spacing: .44em; text-indent: .44em;
    text-transform: uppercase; background: none; border: none; padding: 8px 4px 2px; }
  #coverPage.coverV2 .cvCue:hover { color: #ecd9a2; }
  #coverPage.coverV2 .cvCue i { width: 16px; height: 9px; border-left: 1.5px solid #d4af37;
    border-bottom: 1.5px solid #d4af37; transform: rotate(-45deg); margin-top: 2px;
    animation: cvFloat 2.2s ease-in-out infinite; opacity: .9; }

  /* --- scroll-reveal transitions --- */
  #coverPage.coverV2 .reveal { opacity: 0; transform: translateY(30px);
    transition: opacity .9s cubic-bezier(.16,.7,.25,1), transform .9s cubic-bezier(.16,.7,.25,1);
    transition-delay: calc(var(--i, 0) * 90ms); }
  #coverPage.coverV2 .reveal.in { opacity: 1; transform: none; }

  @keyframes cvShimmer { 0% { background-position: 0% 50%; } 100% { background-position: 220% 50%; } }
  @keyframes cvFloat  { 0%, 100% { transform: translateY(0) rotate(-45deg); opacity: .45; }
                         50% { transform: translateY(6px) rotate(-45deg); opacity: 1; } }
  @keyframes cvGlow   { 0%, 100% { box-shadow: 0 18px 44px rgba(0,0,0,.5), 0 0 14px rgba(212,175,55,.14),
                                      inset 0 0 24px rgba(212,175,55,.07); }
                         50% { box-shadow: 0 18px 44px rgba(0,0,0,.5), 0 0 36px rgba(212,175,55,.42),
                                      inset 0 0 30px rgba(212,175,55,.13); } }

  @media (max-width: 900px) {
    #coverPage.coverV2 .cvWhat { grid-template-columns: 1fr; }
    #coverPage.coverV2 .cvWhatCard:nth-child(5) { grid-column: auto; }
  }
  @media (max-width: 760px) {
    #coverPage.coverV2 .cvFeats { grid-template-columns: 1fr; max-width: 500px; }
    #coverPage.coverV2 .cvWrap { gap: clamp(34px, 6vh, 52px); padding-top: clamp(44px, 9vh, 80px); }
  }
  @media (prefers-reduced-motion: reduce) {
    #coverPage.coverV2 .cvTitle .a, #coverPage.coverV2 .cvBtn { animation: none; }
    #coverPage.coverV2 .cvBtn::after { display: none; }
    #coverPage.coverV2 .cvCue i { animation: none; }
    #coverPage.coverV2 .reveal { opacity: 1; transform: none; transition: none; }
    #coverPage.coverV2 { transition-duration: .25s; }
  }

  /* --- v2 additions: jump-to-fabric button + shiny quote --- */
  #coverPage.coverV2 .cvCta { gap: clamp(13px, 2.2vh, 20px); }
  #coverPage.coverV2 .cvJump { position: relative; overflow: hidden; cursor: pointer;
    display: inline-flex; align-items: center; gap: 10px;
    font-family: "Inter", "Segoe UI", sans-serif; font-size: 11px; font-weight: 700;
    letter-spacing: .28em; text-indent: .28em; text-transform: uppercase; color: #1d1403;
    background: linear-gradient(135deg, #f6e6ad 0%, #d4af37 40%, #c0962c 72%, #e8c988 100%);
    border: 1px solid rgba(255,238,190,.95); border-radius: 999px;
    padding: 13px 36px 12px;
    box-shadow: 0 12px 30px rgba(0,0,0,.4), 0 0 20px rgba(212,175,55,.28), inset 0 1px 0 rgba(255,255,255,.5);
    transition: filter .2s, transform .15s, box-shadow .3s; }
  #coverPage.coverV2 .cvJump::after { content: ""; position: absolute; top: 0; left: -90%; width: 55%; height: 100%;
    background: linear-gradient(100deg, transparent, rgba(255,255,255,.75), transparent);
    transform: skewX(-20deg); transition: left .5s ease; }
  #coverPage.coverV2 .cvJump:hover { filter: brightness(1.1); transform: translateY(-2px);
    box-shadow: 0 16px 38px rgba(0,0,0,.45), 0 0 34px rgba(232,201,136,.65), inset 0 1px 0 rgba(255,255,255,.6); }
  #coverPage.coverV2 .cvJump:hover::after { left: 145%; }
  #coverPage.coverV2 .cvJump:active { transform: scale(.97); }
  #coverPage.coverV2 .cvJump::before { content: ""; position: absolute; inset: -40%;
    background: radial-gradient(circle at 50% 0%, rgba(255,255,255,.28), transparent 45%);
    opacity: 0; transition: opacity .3s; pointer-events: none; }
  #coverPage.coverV2 .cvJump:hover::before { opacity: 1; }

  #coverPage.coverV2 .cvQuote { position: relative; margin-top: clamp(12px, 2.4vh, 22px);
    font-family: "Cormorant Garamond", Georgia, serif; font-style: italic; font-weight: 500;
    font-size: clamp(1.12rem, 2vw, 1.5rem); line-height: 1.5; max-width: 640px;
    color: transparent; background: linear-gradient(100deg, #f4f6fb 0%, #f4f6fb 40%, #ffd98a 50%, #f4f6fb 60%, #f4f6fb 100%);
    background-size: 220% 100%; -webkit-background-clip: text; background-clip: text;
    animation: cvQuoteShine 4.2s linear infinite;
    filter: drop-shadow(0 0 16px rgba(212,175,55,.18)); }
  #coverPage.coverV2 .cvQuoteMark { font-style: normal; color: #d4af37; -webkit-text-fill-color: #d4af37;
    text-shadow: 0 0 14px rgba(212,175,55,.6); }
  #coverPage.coverV2 .cvQuoteBy { display: block; margin-top: 10px;
    font-family: "Inter", "Segoe UI", sans-serif; font-style: normal; font-weight: 600;
    font-size: 9px; letter-spacing: .42em; text-indent: .42em; text-transform: uppercase;
    color: #b9a878; -webkit-text-fill-color: #b9a878; }
  @keyframes cvQuoteShine { 0% { background-position: 0% 50%; } 100% { background-position: 220% 50%; } }
  @media (prefers-reduced-motion: reduce) {
    #coverPage.coverV2 .cvQuote { animation: none; background: #f4f6fb; -webkit-text-fill-color: #f4f6fb; color: #f4f6fb; }
  }

  /* ================================================================== */
  /* Metallic gold polish — buttons read as brushed liquid metal        */
  /* ================================================================== */
  #coverPage.coverV2 .cvBtn, #coverPage.coverV2 .cvJump {
    font-family: "Cormorant Garamond", Georgia, serif; font-weight: 600; }

  /* primary — bright brushed-gold metal, espresso ink */
  #coverPage.coverV2 .cvBtn { color: #2b1e02; border: 1px solid rgba(255,244,208,.85);
    font-size: clamp(12px, 1.15vw, 14.5px); letter-spacing: .3em; text-indent: .3em;
    background:
      linear-gradient(180deg, rgba(255,255,255,.6), rgba(255,255,255,0) 40%),
      repeating-linear-gradient(115deg, rgba(255,255,255,.06) 0 2px, rgba(140,105,20,.06) 2px 4px),
      linear-gradient(180deg, #fcecaa 0%, #f4d677 22%, #d4af37 50%, #ab831f 79%, #86640f 100%);
    text-shadow: 0 1px 0 rgba(255,246,214,.6);
    box-shadow: 0 20px 46px rgba(0,0,0,.5), 0 0 20px rgba(212,175,55,.32),
      inset 0 1px 0 rgba(255,255,255,.8), inset 0 -2px 4px rgba(90,64,8,.55),
      inset 0 0 0 1px rgba(120,90,20,.28);
    animation: cvMetalBreath 5.5s ease-in-out infinite; }
  @keyframes cvMetalBreath {
    0%, 100% { box-shadow: 0 20px 46px rgba(0,0,0,.5), 0 0 18px rgba(212,175,55,.3),
      inset 0 1px 0 rgba(255,255,255,.8), inset 0 -2px 4px rgba(90,64,8,.55),
      inset 0 0 0 1px rgba(120,90,20,.28); }
    50% { box-shadow: 0 22px 52px rgba(0,0,0,.55), 0 0 40px rgba(232,201,136,.55),
      inset 0 1px 0 rgba(255,255,255,.92), inset 0 -2px 4px rgba(90,64,8,.5),
      inset 0 0 0 1px rgba(120,90,20,.32); } }
  #coverPage.coverV2 .cvBtn:hover { filter: brightness(1.08); transform: translateY(-2px);
    animation-play-state: paused;
    box-shadow: 0 24px 56px rgba(0,0,0,.55), 0 0 48px rgba(232,201,136,.65),
      inset 0 1px 0 rgba(255,255,255,.95), inset 0 -2px 4px rgba(90,64,8,.5),
      inset 0 0 0 1px rgba(120,90,20,.3); }
  #coverPage.coverV2 .cvBtn:active { transform: scale(.96); }

  /* secondary — dark antique-bronze metal, champagne ink */
  #coverPage.coverV2 .cvJump { color: #f3e1a3; border: 1px solid rgba(255,236,178,.55);
    font-size: clamp(11px, 1.05vw, 13px); letter-spacing: .26em; text-indent: .26em;
    background:
      linear-gradient(180deg, rgba(255,255,255,.22), rgba(255,255,255,0) 42%),
      repeating-linear-gradient(115deg, rgba(255,255,255,.035) 0 2px, rgba(0,0,0,.1) 2px 4px),
      linear-gradient(180deg, #43330d 0%, #6b541d 26%, #9a7c31 52%, #6b541d 76%, #322509 100%);
    text-shadow: 0 1px 2px rgba(0,0,0,.6), 0 0 14px rgba(212,175,55,.18);
    box-shadow: 0 14px 34px rgba(0,0,0,.45), 0 0 14px rgba(212,175,55,.16),
      inset 0 1px 0 rgba(255,255,255,.32), inset 0 -2px 5px rgba(0,0,0,.55),
      inset 0 0 0 1px rgba(255,255,255,.05); }
  #coverPage.coverV2 .cvJump:hover { filter: brightness(1.16); transform: translateY(-2px);
    border-color: rgba(255,242,205,.9);
    box-shadow: 0 18px 42px rgba(0,0,0,.5), 0 0 32px rgba(232,201,136,.45),
      inset 0 1px 0 rgba(255,255,255,.5), inset 0 -2px 5px rgba(0,0,0,.45),
      inset 0 0 0 1px rgba(255,255,255,.12); }
  #coverPage.coverV2 .cvJump:active { transform: scale(.96); }
  #coverPage.coverV2 .cvJump::after { background: linear-gradient(100deg, transparent, rgba(255,255,255,.55), transparent); }

  @media (prefers-reduced-motion: reduce) {
    #coverPage.coverV2 .cvBtn { animation: none; }
  }

  /* ================================================================== */
  /* Refined buttons — dark glass + metallic gold touch, bright type    */
  /* ================================================================== */
  #coverPage.coverV2 .cvBtn, #coverPage.coverV2 .cvJump {
    font-family: "Cormorant Garamond", Georgia, serif; font-weight: 700;
    background-size: 260% 100%, 100% 100%, 100% 100%, 100% 100%;
    animation: cvBtnSheen 6.5s ease-in-out infinite; }
  @keyframes cvBtnSheen {
    0%   { background-position: -70% 0, 0 0, 0 0, 0 0; }
    10%  { background-position: 170% 0, 0 0, 0 0, 0 0; }
    100% { background-position: 170% 0, 0 0, 0 0, 0 0; } }

  /* primary — luminous champagne text on dark glass */
  #coverPage.coverV2 .cvBtn { color: #fff6dd;
    font-size: clamp(12.5px, 1.2vw, 15px); letter-spacing: .28em; text-indent: .28em;
    text-shadow: 0 0 8px rgba(255,240,200,.45), 0 2px 10px rgba(0,0,0,.65);
    border: 1px solid rgba(240,213,152,.9);
    background:
      linear-gradient(105deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 40%,
                      rgba(255,244,205,.22) 50%, rgba(255,255,255,0) 60%, rgba(255,255,255,0) 100%),
      linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,0) 46%),
      radial-gradient(130% 200% at 50% -30%, rgba(212,175,55,.32), rgba(212,175,55,.06) 52%, transparent 80%),
      linear-gradient(180deg, rgba(20,15,6,.85), rgba(6,6,10,.9));
    box-shadow: 0 16px 42px rgba(0,0,0,.5), 0 0 20px rgba(212,175,55,.28),
      inset 0 1px 0 rgba(255,255,255,.35), inset 0 -1px 3px rgba(0,0,0,.45),
      inset 0 0 0 1px rgba(255,255,255,.05); }
  #coverPage.coverV2 .cvBtn::after { background: linear-gradient(100deg, transparent, rgba(255,255,255,.2), transparent); }
  #coverPage.coverV2 .cvBtn:hover { animation-play-state: paused; filter: brightness(1.1); transform: translateY(-2px);
    border-color: #ffe9ae; box-shadow: 0 20px 50px rgba(0,0,0,.55), 0 0 40px rgba(232,201,136,.5),
      inset 0 1px 0 rgba(255,255,255,.45), inset 0 -1px 3px rgba(0,0,0,.4); }
  #coverPage.coverV2 .cvBtn:active { transform: scale(.96); }

  /* secondary — same language, quieter gold */
  #coverPage.coverV2 .cvJump { color: #f6e9c4;
    font-size: clamp(11.5px, 1.1vw, 13.5px); letter-spacing: .24em; text-indent: .24em;
    text-shadow: 0 0 7px rgba(255,236,180,.4), 0 2px 9px rgba(0,0,0,.6);
    border: 1px solid rgba(232,201,136,.6);
    background:
      linear-gradient(105deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0) 40%,
                      rgba(255,244,205,.15) 50%, rgba(255,255,255,0) 60%, rgba(255,255,255,0) 100%),
      linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,0) 46%),
      radial-gradient(130% 200% at 50% -30%, rgba(212,175,55,.2), rgba(212,175,55,.04) 55%, transparent 80%),
      linear-gradient(180deg, rgba(14,11,4,.8), rgba(5,5,9,.86));
    box-shadow: 0 12px 32px rgba(0,0,0,.45), 0 0 12px rgba(212,175,55,.14),
      inset 0 1px 0 rgba(255,255,255,.24), inset 0 -1px 3px rgba(0,0,0,.4); }
  #coverPage.coverV2 .cvJump::after { background: linear-gradient(100deg, transparent, rgba(255,255,255,.14), transparent); }
  #coverPage.coverV2 .cvJump:hover { animation-play-state: paused; filter: brightness(1.12); transform: translateY(-2px);
    border-color: rgba(255,233,170,.85); box-shadow: 0 16px 40px rgba(0,0,0,.5), 0 0 26px rgba(232,201,136,.35),
      inset 0 1px 0 rgba(255,255,255,.34), inset 0 -1px 3px rgba(0,0,0,.4); }
  #coverPage.coverV2 .cvJump:active { transform: scale(.96); }

  @media (prefers-reduced-motion: reduce) {
    #coverPage.coverV2 .cvBtn, #coverPage.coverV2 .cvJump { animation: none; background-position: -70% 0, 0 0, 0 0, 0 0; }
  }

  /* --- in-simulator "Back to Base-1" — same design family as the cover CTAs --- */
  #panel .btnBack { width: 100%; display: flex; align-items: center; justify-content: center; gap: 8px;
    margin: 0 0 10px; padding: 9px 14px 8px; cursor: pointer;
    font-family: "Cormorant Garamond", Georgia, serif; font-weight: 700;
    font-size: 12px; letter-spacing: .22em; text-indent: .22em; text-transform: uppercase;
    color: #f4e2ab; background: linear-gradient(180deg, rgba(255,255,255,.07), rgba(255,255,255,0) 55%), rgba(5,8,14,.65);
    border: 1px solid rgba(212,175,55,.55); border-radius: 999px;
    box-shadow: inset 0 1px 0 rgba(255,255,255,.14), 0 0 0 rgba(212,175,55,0);
    transition: filter .18s, transform .12s, box-shadow .3s, border-color .3s; }
  #panel .btnBack:hover { filter: brightness(1.18); border-color: rgba(232,201,136,.95);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.2), 0 0 16px rgba(212,175,55,.4); }
  #panel .btnBack:active { transform: scale(.97); }
  @media (prefers-reduced-motion: reduce) {
    #panel .btnBack { transition: filter .15s, transform .05s; }
  }
  /* live space background is decorative only — never intercepts cover clicks */
  #coverStars { pointer-events: none; }
</style>
</head>
<body>

<div id="coverPage" class="coverV2" aria-label="Techsense Project — Multi-Axis Fabric Model">
  <canvas id="coverStars" aria-hidden="true"></canvas>
  <div class="cvScroll">
    <div class="cvWrap">
      <header class="cvHead">
        <h1 class="cvTitle">
          <span class="a">TECHSENSE PROJECT</span>
          <span class="b">MULTI-AXIS FABRIC MODEL</span>
        </h1>
        <div class="cvRule"></div>
        <p class="cvSub">A Visual Study in Curved Spacetime</p>
      </header>
      <p class="cvLead">Spacetime is not a passive backdrop. <strong>Mass and energy curve it — and that curvature <em>is</em> gravity.</strong> This model renders that curvature as a literal, woven fabric: a Flamm-paraboloid sheet and a three-dimensional lattice you can rotate, zoom into, and watch deform in real time.</p>
      <p class="cvBasis">Built on <b>Einstein&rsquo;s field equations</b>, with light&rsquo;s path governed by the <b>Lucky Deflection Formula</b> &mdash; <span class="fx">&theta; = (4GM/c&sup2;b)(1 + &Delta;)</span> &mdash; an original modified-gravity ansatz with a compactified extra dimension.</p>
      <div class="cvFeats">
        <div class="cvFeat">
          <svg class="cvIcon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" aria-hidden="true"><circle cx="16" cy="16" r="2.6"/><circle cx="16" cy="16" r="7.4"/><circle cx="16" cy="16" r="12.6"/></svg>
          <h3>Gravitational Pull, Made Visible</h3>
          <p>Drop a star, black hole, or neutron star into the lattice and watch it carve a well that drags passing light and matter along curved paths — curvature you can orbit instead of only calculate.</p>
        </div>
        <div class="cvFeat">
          <svg class="cvIcon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 4.5 27 10v12L16 27.5 5 22V10Z"/><path d="M5 10l11 6 11-6M16 16v11.5"/></svg>
          <h3>Hidden Dimensions, Made Visible</h3>
          <p>The model carries a compactified fifth (W) spatial dimension that stays curled and invisible under ordinary conditions — until sufficiently dense mass opens it and extrudes geometry the equations otherwise hide.</p>
        </div>
        <div class="cvFeat">
          <svg class="cvIcon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" aria-hidden="true"><path d="M6 6h20M6 16h20M6 26h20M6 6v20M16 6v20M26 6v20"/></svg>
          <h3>The Fabric, as a Real Object</h3>
          <p>Not a decorative grid: a driven, physically parameterized lattice whose metric controls — n, Φ₀, α, ℓ — stay live-adjustable as it breathes, ripples, and twists to the field equations.</p>
        </div>
      </div>
      <p class="cvNote"><i>The two- and three-dimensional fabric is the complete, present core of the project; the full five-dimensional view is included here as an early preview of the model&rsquo;s next stage.</i></p>
      <div class="cvCta">
        <button class="cvBtn cvEnter" id="coverCta" type="button">Enter the Simulation</button>
        <button class="cvJump cvEnter" id="coverJump5d" type="button" data-view="cubic" title="Skips the intro and drops you straight into the interactive cubic-lattice view of the fabric">&#11041; Jump to the 5D Fabric</button>
        <span class="cvPill"><i></i>5D Model &mdash; Upcoming</span>
        <p class="cvQuote"><span class="cvQuoteMark">&ldquo;</span>Spacetime tells matter how to move;<br />matter tells spacetime how to curve.<span class="cvQuoteMark">&rdquo;</span><span class="cvQuoteBy">John Archibald Wheeler</span></p>
      </div>

      <section class="cvSec" id="cvWhat">
        <header class="cvSecHead reveal">
          <p class="cvSecKicker">Inside the Simulation</p>
          <h2 class="cvSecTitle">What the Fabric Has in Store</h2>
          <div class="cvSecRule"></div>
        </header>
        <div class="cvWhat">
          <article class="cvWhatCard reveal" style="--i:0">
            <span class="cvNum">01</span>
            <div class="cvWhatBody">
              <h3>Mass bends the lattice</h3>
              <p>Drop a Sun, heavy star, black hole or neutron star into the grid &mdash; it sinks a funnel that drags passing light and matter along curved paths.</p>
            </div>
          </article>
          <article class="cvWhatCard reveal" style="--i:1">
            <span class="cvNum">02</span>
            <div class="cvWhatBody">
              <h3>Binaries collide</h3>
              <p>Launch neutron-star or black-hole pairs &mdash; they orbit, inspiral, stretch into teardrops, then merge in a kilonova of jets and fabric ripples.</p>
            </div>
          </article>
          <article class="cvWhatCard reveal" style="--i:2">
            <span class="cvNum">03</span>
            <div class="cvWhatBody">
              <h3>A hidden 5th dimension</h3>
              <p>Four live dials &mdash; n, &Phi;&#8320;, &alpha;, &ell; &mdash; control a compactified W-dimension that visibly extrudes around dense horizons.</p>
            </div>
          </article>
          <article class="cvWhatCard reveal" style="--i:3">
            <span class="cvNum">04</span>
            <div class="cvWhatBody">
              <h3>Light walks geodesics</h3>
              <p>Fire light beams and ambient photon storms across the field and watch them lens around mass &mdash; pure curvature, no strings attached.</p>
            </div>
          </article>
          <article class="cvWhatCard reveal" style="--i:4">
            <span class="cvNum">05</span>
            <div class="cvWhatBody">
              <h3>Horizons evaporate</h3>
              <p>Hawking radiation glows around black holes and can slowly burn them away &mdash; while the TOV limit decides the fate of every merger remnant.</p>
            </div>
          </article>
        </div>
      </section>

      <section class="cvSec cvControls reveal">
        <header class="cvSecHead">
          <p class="cvSecKicker">Flight Manual</p>
          <h2 class="cvSecTitle">Take the Controls</h2>
        </header>
        <ul class="cvKeys">
          <li><b>wheel</b><span>zoom</span></li>
          <li><b>drag</b><span>nudge the view</span></li>
          <li><b>space</b><span>free flight</span></li>
          <li><b>wasd</b><span>fly</span></li>
          <li><b>p</b><span>pause</span></li>
          <li><b>esc</b><span>exit placement</span></li>
        </ul>
      </section>

      <section class="cvOutro reveal">
        <p class="cvOutroLine">Curved. Woven. Alive. <i>Go bend it.</i></p>
        <button class="cvBtn cvEnter" type="button">Launch the Fabric Model</button>
        <span class="cvPill"><i></i>Sheet &middot; Cubic lattice &middot; 5D preview</span>
      </section>

      <footer class="cvFoot">Techsense &middot; Lucky Deflection Model v68 &middot; Single-file WebGL study</footer>
    </div>
  </div>
</div>

<div id="overlay">
  <div class="spinner"></div>
  <h1>⬡ Multi-Axis Spacetime Fabric</h1>
  <p>Loading simulation &mdash; <span id="ovmsg">fetching three.js (internet required on first run)</span>&hellip;</p>
</div>

<div id="panel">
  <div class="head"><h2>⬡ MULTI-AXIS <i>SPACETIME</i> FABRIC</h2><span>LUCKY MODEL v68</span></div>
  <button class="btnBack" id="bBackBase" type="button" title="Return to the Techsense cover page — the simulation stays live underneath">Back to Base-1</button>

  <div class="section">
    <div class="ttl">Fabric view — same simulation, three projections</div>
    <div class="seg" id="viewSeg" style="margin-bottom:8px">
      <div class="segbtn on" data-view="sheet">⛶ 2D–3D grid sheet</div>
      <div class="segbtn" data-view="cubic">⬡ Cubic lattice</div>
      <div class="segbtn" data-view="5d">✴ 5D View<span class="upTag">Upcoming</span></div>
    </div>
    <div class="ttl">Objects</div>
    <div class="btnrow">
      <button class="btn sun" id="bAddSun">☀ Add Solar System</button>
      <button class="btn sun" id="bAddSunStar">✦ Add Sun</button>
      <button class="btn star" id="bAddHeavy">★ Add Heavy Star</button>
      <button class="btn bh" id="bAddBH">◉ Add Black Hole</button>
      <button class="btn ns" id="bAddNS">✳ Add Neutron Star</button>
      <button class="btn ps" id="bAddPulsar">⚡ Add Pulsar</button>
      <button class="btn met" id="bAddMeteors">☄ Add Meteors</button>
      <button class="btn lgt" id="bAddLight">✦ Add Light</button>
      <button class="btn bh" id="bBHBinary" title="Place two black holes on a collision course — same inspiral engine as the NS pair">◉ Add 2 Black Holes</button>
      <button class="btn ns" id="bNSBinary" title="Place two neutron stars in tight binary orbit">✳ Add 2 Neutron Stars</button>
      <button class="btn wide" id="bClear" style="color:#ff9fae">✕ Clear All Objects</button>
    </div>
    <div style="margin-top:8px">
      <div class="ttl" style="margin-bottom:4px">Present</div>
      <div id="objList"><div style="color:#7f93b6;font-size:11px">No masses yet &mdash; pure parallel lattice.</div></div>
      <div id="selCard" hidden>
        <div class="lbl">Selected</div>
        <div class="mono" id="selInfo"></div>
        <label>Mass strength <span class="val" id="selStrVal" style="font-family:Consolas">1.00×</span></label>
        <input type="range" id="selStr" min="0.1" max="4" step="0.05" value="1" />
      </div>
    </div>
  </div>

  <details class="section" open>
    <summary>Fabric Parameters — 5D Metric</summary>
    <div class="slider"><div class="row"><span>n — threshold steepness (6–8)</span><span class="val" id="vN">7.0</span></div>
      <input type="range" id="sN" min="1" max="12" step="0.1" value="7" /></div>
    <div class="slider"><div class="row"><span>Φ₀ — threshold potential</span><span class="val" id="vPhi0">0.080</span></div>
      <input type="range" id="sPhi0" min="0.01" max="0.5" step="0.001" value="0.08" /></div>
    <div class="slider"><div class="row"><span>α — extra-dimension coupling (≤ 0.10)</span><span class="val" id="vAlpha">0.100</span></div>
      <input type="range" id="sAlpha" min="0" max="0.2" step="0.001" value="0.1" /></div>
    <div class="slider"><div class="row"><span>ℓ — extra-dimension size (km)</span><span class="val" id="vL">4.0</span></div>
      <input type="range" id="sL" min="1" max="20" step="0.5" value="4" /></div>
    <div class="slider"><div class="row"><span>Mass warp strength ×</span><span class="val" id="vWarp">1.0</span></div>
      <input type="range" id="sWarp" min="0" max="6" step="0.05" value="1" /></div>
    <div class="slider"><div class="row"><span>Distortion amplitude</span><span class="val" id="vDist">1.6</span></div>
      <input type="range" id="sDist" min="0" max="4" step="0.05" value="1.6" /></div>
    <div class="slider"><div class="row"><span>W-extrusion scale</span><span class="val" id="vWSc">1.8</span></div>
      <input type="range" id="sWSc" min="0" max="4" step="0.05" value="1.8" /></div>
    <div class="slider"><div class="row"><span>Well depth (sheet view)</span><span class="val" id="vWell">1.00</span></div>
      <input type="range" id="sWell" min="0" max="3" step="0.05" value="1" /></div>
    <div class="slider"><div class="row"><span>Traveling wave speed</span><span class="val" id="vWave">1.0</span></div>
      <input type="range" id="sWave" min="0" max="3" step="0.05" value="1" /></div>
    <div class="slider"><div class="row"><span>Fabric breathing</span><span class="val" id="vBreath">0.6</span></div>
      <input type="range" id="sBreath" min="0" max="1" step="0.02" value="0.6" /></div>
    <div class="slider"><div class="row"><span>Infinite-fade distance</span><span class="val" id="vFade">24.0</span></div>
      <input type="range" id="sFade" min="6" max="40" step="0.5" value="24" /></div>
    <div class="slider"><div class="row"><span>Lattice density</span><span class="val" id="vDens">1.00</span></div>
      <input type="range" id="sDens" min="0.25" max="1" step="0.05" value="1" /></div>
    <div class="slider"><div class="row"><span>Deep nesting (4th level)</span></div>
      <input type="checkbox" id="sNest" style="margin-top:2px" /></div>
    <div class="slider"><div class="row"><span>Hawking evaporation</span></div>
      <input type="checkbox" id="sEvap" style="margin-top:2px" /><span style="font-size:10px;color:#7f93b6;margin-left:6px">BH slowly loses mass</span></div>
    <div class="slider"><div class="row"><span>Background</span></div>
      <select id="sBg">
        <option value="white">Pure white void</option>
        <option value="offwhite">Off-white studio</option>
        <option value="dark" selected>Graphite (dark)</option>
      </select></div>
  </details>

  <details class="section" open>
    <summary>Camera &amp; Rendering</summary>
    <div class="seg" id="camSeg" style="margin-bottom:8px">
      <div class="segbtn on" data-cam="cinematic">◈ Cinematic drift</div>
      <div class="segbtn" data-cam="free">✦ Free flight</div>
    </div>
    <div class="slider"><div class="row"><span>Simulation speed</span><span class="val" id="vTime">1.0</span></div>
      <input type="range" id="sTime" min="0" max="3" step="0.05" value="1" /></div>
    <div class="slider"><div class="row"><span>Flight speed</span><span class="val" id="vFly">3.0</span></div>
      <input type="range" id="sFly" min="1" max="16" step="0.5" value="3" /></div>
    <div class="slider"><div class="row"><span>Bloom strength</span><span class="val" id="vBloom">0.12</span></div>
      <input type="range" id="sBloom" min="0" max="1.5" step="0.05" value="0.12" /></div>
    <div class="slider"><div class="row"><span>Planet detail</span><span class="val" id="vPlanet">1.50×</span></div>
      <input type="range" id="sPlanet" min="0.5" max="2" step="0.25" value="1.5" /></div>
    <div class="slider"><div class="row"><span>Quality (8K capable)</span></div>
      <select id="sQual">
        <option value="0.75">Low</option>
        <option value="1" selected>Balanced</option>
        <option value="1.5">High</option>
        <option value="2">Ultra</option>
        <option value="3.2">8K scale</option>
      </select></div>
  </details>

  <details class="section" open>
    <summary>Readout</summary>
    <div id="readout"></div>
  </details>

  <details class="section">
    <summary>Lucky Deflection — Formulas</summary>
    <div style="font-family:Consolas,monospace;font-size:10.5px;line-height:1.7;color:#d6eaff;padding-top:6px">
      <div style="color:#7f93b6;font-size:9.5px;letter-spacing:1.2px;margin-bottom:3px">SIMPLE FORM</div>
      θ_Lucky = (4GM / c²b) · (1 + Δ)<br>
      Δ = 0.90 · α · (Φ<sub>b</sub>/Φ₀)ⁿ / (1 + (Φ<sub>b</sub>/Φ₀)ⁿ)<br>
      Φ<sub>b</sub> = GM / (c²b) &nbsp;·&nbsp; b = impact parameter<br>
      <div style="color:#7f93b6;font-size:9.5px;letter-spacing:1.2px;margin:9px 0 3px">COMPLEX GEODESIC FORM</div>
      Null geodesics of the 5D metric, ds² = 0:<br>
      ds² = −A(r)c²dt² + B(r)dr² + r²dΩ² + D(r)dw²<br>
      d²x<sup>μ</sup>/dλ² + Γ<sup>μ</sup><sub>αβ</sub> (dx<sup>α</sup>/dλ)(dx<sup>β</sup>/dλ) = 0<br><br>
      Bending integral (exact null geodesic of the static spherical metric):<br>
      Δφ = 2 ∫<sub>r₀</sub><sup>∞</sup> [ b √(A(r)·B(r)) / ( r² √( 1 − b²·A(r)/r² ) ) ] dr − π<br><br>
      b = r₀ / √A(r₀) &nbsp;·&nbsp; Φ(r) = GM / (c²r)<br>
      Δ(r) = 0.90 · α · (Φ(r)/Φ₀)ⁿ / (1 + (Φ(r)/Φ₀)ⁿ)<br>
      D(r) = ℓ² [ 1 + α (Φ/Φ₀)ⁿ / (1 + (Φ/Φ₀)ⁿ) ]<br>
      Schwarzschild A = 1 − 2GM/c²r, B = 1/A &nbsp;⇒&nbsp; θ<sub>Einstein</sub> = 4GM/(c²b)<br>
      <span style="color:#7f93b6">W-closed limit D(r)→ℓ², Δ→0 recovers the classical 4D Einstein bending.</span>
    </div>
  </details>
</div>

<div id="banner"></div>
<div id="hint">◈ Cinematic drift &mdash; wheel: zoom · drag: nudge · P: pause · Space: free flight</div>
<div id="details" class="hidden">
  <div class="dHead"><h3 id="dTitle">—</h3><button class="close" id="dClose">✕</button></div>
  <div id="dBody"></div>
</div>
<div id="fps">-- fps</div>

<script>
/* ============================================================================
   MULTI-AXIS SPACETIME FABRIC — "Lucky Model v68"
   ----------------------------------------------------------------------------
   Exact physics implemented:

     Metric ansatz:
       ds² = −A(r) c² dt² + B(r) dr² + r² dΩ² + D(r) dw²

     Extra-dimension size (threshold form):
       D(r) = ℓ² [ 1 + α · (Φ/Φ₀)ⁿ / (1 + (Φ/Φ₀)ⁿ) ],   Φ = GM / (c² r)

     Lucky Deflection Formula (practical working version):
       θ_Lucky = (4GM / c² b) (1 + Δ)
       Δ ≈ 0.90 × α · (Φ_b / Φ₀)ⁿ / (1 + (Φ_b / Φ₀)ⁿ)

     Default parameter window (user-adjustable in real time):
       n = 6–8, Φ₀ = 0.075–0.085, α ≤ 0.10, ℓ ≲ 3–5 km

   Weak-field safety: the Sun's physical compactness GM/c²R ≈ 2.5e-6 keeps\n'
   'Φ ≪ Φ₀ at Solar-System scales, so Δ ~ 10⁻³³ (the spec's 10⁻²⁸–10⁻³⁴ band)
   and the fabric stays perfectly parallel. Black holes / neutron stars push
   Φ past the threshold, opening D(r) and extruding the W-dimension edges.
   Every dynamical integrator (planets, meteors, tidal streams, mergers,
   photons) uses the same (1 + Δ) effective potential: a = GM(1+Δ)/r² with Δ
   evaluated at the local Φ, and light follows null geodesics (|v| = c) so the
   observed bending is purely the projection of the opened W-dimension.
   ============================================================================ */

/* Embedded JSON configuration — the default parameter window (also editable
   live from the panel; JSON so the file is data-driven and re-runnable). */
const CONFIG = {
  metric: { n: 7.0, phi0: 0.080, alpha: 0.100, ell: 4.0 },
  visual: { warpMul: 1.0, distort: 1.6, wScale: 1.8, wave: 1.0, breath: 0.6, fade: 24.0, density: 1.0, deepNest: false, bg: "dark", view: "sheet", wellDepth: 1.0 },
  camera: { mode: "cinematic", timeScale: 1.0, flySpeed: 3.0, dof: false, aperture: 0.0016, bloom: 0.12, quality: 1, planetDetail: 1.5 },
  bodies: { maxMajor: 8, maxBeams: 6, maxMeteors: 60 },
  lattice: { L: 1.6, N: 20, MAXM: 8 }
};

/* ------------------------------------------------------------------ */
/* 0. Deferred bootstrap (cover-first)                                */
/* ------------------------------------------------------------------ */
/* Chosen approach: DEFER (see §4.1). The visitor's first screen is the
   cover page; three.js is only fetched from CDN and the scene is only
   built once the "ENTER THE SIMULATION" CTA is clicked (section 17).
   simBooted guards against double invocation if the CTA ever fires
   twice. All DOM lookups below happen at call time, when the static
   markup is long since parsed, so nothing regresses. */
let simBooted = false;
async function bootSimulator() {

/* ------------------------------------------------------------------ */
/* 1. Load three.js (multiple CDN fallbacks)                          */
/* ------------------------------------------------------------------ */
/* esm.sh first: it rewrites bare specifiers, so the addon modules resolve to the
   same three.js instance. unpkg/jsdelivr serve raw ESM that imports 'three' by
   bare name and only work behind an import map — kept as fallbacks. */
const CDNS = [
  { three: "https://esm.sh/three@0.160.0", addons: "https://esm.sh/three@0.160.0/examples/jsm/" },
  { three: "https://unpkg.com/three@0.160.0/build/three.module.js", addons: "https://unpkg.com/three@0.160.0/examples/jsm/" },
  { three: "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js", addons: "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/" }
];
const ov = document.getElementById("ovmsg");
let THREE = null, EffectComposer, RenderPass, UnrealBloomPass, OutputPass;
for (const cdn of CDNS) {
  try {
    /* load the WHOLE set from one CDN atomically so instances never mix */
    const m = await import(cdn.three);
    const EC = await import(cdn.addons + "postprocessing/EffectComposer.js");
    const RP = await import(cdn.addons + "postprocessing/RenderPass.js");
    const UB = await import(cdn.addons + "postprocessing/UnrealBloomPass.js");
    const OP = await import(cdn.addons + "postprocessing/OutputPass.js");
    THREE = m;
    EffectComposer = EC.EffectComposer;
    RenderPass = RP.RenderPass;
    UnrealBloomPass = UB.UnrealBloomPass;
    OutputPass = OP.OutputPass;
    break;
  } catch (e) { THREE = null; }
}
if (!THREE) {
  document.getElementById("overlay").innerHTML =
    "<h1 class='err'>Could not load three.js</h1><p>This file needs an internet connection on first run " +
    "(the three.js library is fetched from a CDN). Check your connection and reload.</p>";
  return;
}
document.getElementById("overlay").style.display = "none";

/* ------------------------------------------------------------------ */
/* 2. Renderer / scene / camera / post-processing                     */
/* ------------------------------------------------------------------ */
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(2, CONFIG.camera.quality * (window.devicePixelRatio || 1)));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.NoToneMapping;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xffffff);

const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.05, 500);
camera.position.set(10, 6.5, 14);

const composer = new EffectComposer(renderer);
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

const bloomPass = new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 0.12, 0.7, 0.7);
composer.addPass(bloomPass);

/* depth of field is intentionally NOT used — the fabric and all objects must
   stay razor-sharp at every zoom level (no blur, no softening) */
composer.addPass(new OutputPass());

const BG = { white: 0xffffff, offwhite: 0xeef3fb, dark: 0x000000 };
function applyBg(mode) {
  /* "dark" is 0x000000 — a falsy value, so never use `||` here or dark mode
     silently falls back to white */
  const hex = (mode in BG) ? BG[mode] : 0xffffff;
  scene.background.setHex(hex);
  fabricMats.forEach(m => m.uniforms.uBg.value.setHex(hex));
  document.body.style.background = "#" + hex.toString(16).padStart(6, "0");
  /* bloom is counter-productive against a bright void; modest boost in dark mode */
  bloomPass.strength = (mode === "dark" ? Math.max(CONFIG.camera.bloom, 0.2) : CONFIG.camera.bloom);
}

/* Lights (affect only the celestial standard-material objects) */
scene.add(new THREE.AmbientLight(0xffffff, 0.55));
const keyLight = new THREE.DirectionalLight(0xffffff, 1.15); keyLight.position.set(6, 10, 4); scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0xbfd4ff, 0.45); fillLight.position.set(-5, -4, -3); scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0xffffff, 0.4); rimLight.position.set(-3, 5, -6); scene.add(rimLight);

/* ------------------------------------------------------------------ */
/* 3. Procedural textures                                             */
/* ------------------------------------------------------------------ */
function glowTexture(inner, outer) {
  const c = document.createElement("canvas"); c.width = c.height = 64;
  const g = c.getContext("2d");
  const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, inner); gr.addColorStop(0.35, outer); gr.addColorStop(1, "rgba(0,0,0,0)");
  g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
  const t = new THREE.CanvasTexture(c);
  t.generateMipmaps = false; t.minFilter = THREE.LinearFilter;   // crisp, no mipmap blur
  return t;
}
const glowWhite = glowTexture("rgba(255,255,255,1)", "rgba(255,255,255,0.28)");
const glowCyan  = glowTexture("rgba(214,250,255,1)", "rgba(90,220,255,0.25)");
const glowRed   = glowTexture("rgba(255,235,238,1)", "rgba(255,80,110,0.25)");
const glowOran  = glowTexture("rgba(255,246,228,1)", "rgba(255,150,70,0.3)");

function sunTexture(inner, mid, outer) {
  const c = document.createElement("canvas"); c.width = c.height = 256;
  const g = c.getContext("2d");
  const i = inner || "#fffbe8", m = mid || "#ffe9a8", o = outer || "#ff9a3c";
  const gr = g.createRadialGradient(128, 128, 8, 128, 128, 128);
  gr.addColorStop(0, i); gr.addColorStop(0.35, m); gr.addColorStop(0.7, "#ffc36b"); gr.addColorStop(1, o);
  g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 900; i++) {
    const a = Math.random() * Math.PI * 2, r = Math.pow(Math.random(), 0.7) * 122;
    g.fillStyle = "rgba(255," + (120 + Math.floor(Math.random() * 80)) + ",60," + (0.05 + Math.random() * 0.14) + ")";
    g.beginPath(); g.arc(128 + r * Math.cos(a), 128 + r * Math.sin(a), 1 + Math.random() * 2.4, 0, 7); g.fill();
  }
  const t = new THREE.CanvasTexture(c);
  t.generateMipmaps = false; t.minFilter = THREE.LinearFilter;   // razor-sharp at any distance
  return t;
}

function rockTexture() {
  const c = document.createElement("canvas"); c.width = c.height = 128;
  const g = c.getContext("2d");
  g.fillStyle = "#7d7463"; g.fillRect(0, 0, 128, 128);
  for (let i = 0; i < 1600; i++) {
    const v = 70 + Math.random() * 80;
    g.fillStyle = "rgba(" + v + "," + (v - 8) + "," + (v - 22) + "," + (0.12 + Math.random() * 0.25) + ")";
    g.fillRect(Math.random() * 128, Math.random() * 128, 1.5 + Math.random() * 2.5, 1.5 + Math.random() * 2.5);
  }
  for (let i = 0; i < 26; i++) {
    const x = Math.random() * 128, y = Math.random() * 128, r = 2 + Math.random() * 7;
    g.fillStyle = "rgba(40,36,30," + (0.25 + Math.random() * 0.35) + ")";
    g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
    g.strokeStyle = "rgba(190,180,160,0.35)";
    g.lineWidth = 1; g.stroke();
  }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.generateMipmaps = false; t.minFilter = THREE.LinearFilter;   // crisp at any distance
  return t;
}
const rockTex = rockTexture();

/* Procedural planet surfaces — every world gets real texture detail (craters,
   continents, clouds, storm bands) instead of a flat tint, so planets stay
   crisp and identifiable at any zoom. Resolution scales with the Planet detail
   slider (CONFIG.camera.planetDetail). */
function planetTexture(def, res) {
  const c = document.createElement("canvas"); c.width = c.height = res;
  const g = c.getContext("2d");
  const base = new THREE.Color(def.color);
  const hue = base.getHSL({});
  const R = (a) => Math.random() * a;
  const shade = (mul) => {
    const h = hue.h + (R(0.03) - 0.015);
    const s = Math.min(1, Math.max(0, hue.s + (R(0.14) - 0.07)));
    const l = Math.min(0.95, Math.max(0.06, hue.l * mul));
    return "hsl(" + (h * 360).toFixed(1) + "," + (s * 100).toFixed(1) + "%," + (l * 100).toFixed(1) + "%)";
  };
  g.fillStyle = shade(1); g.fillRect(0, 0, res, res);
  const type = def.tex || "rocky";
  if (type === "earth") {
    g.fillStyle = "#1d5fc4"; g.fillRect(0, 0, res, res);
    for (let i = 0; i < 46; i++) {
      const x = R(res), y = R(res), r = 7 + R(res * 0.17);
      g.fillStyle = R(1) < 0.7 ? "hsl(120,45%," + (24 + R(12)) + "%)" : "hsl(38,55%," + (46 + R(16)) + "%)";
      g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
      g.fillStyle = "rgba(0,0,0,0.10)"; g.beginPath(); g.arc(x + r * 0.3, y + r * 0.25, r * 0.55, 0, 7); g.fill();
    }
    g.fillStyle = "rgba(255,255,255,0.88)"; g.fillRect(0, 0, res, res * 0.075); g.fillRect(0, res * 0.925, res, res * 0.075);
    g.strokeStyle = "rgba(255,255,255,0.32)"; g.lineWidth = res * 0.012;
    for (let i = 0; i < 16; i++) {
      const y0 = R(res), x0 = R(res);
      g.beginPath(); g.moveTo(x0, y0);
      for (let s = 0; s < 5; s++) g.lineTo(x0 + R(res * 0.22) - res * 0.11, y0 + s * res * 0.05);
      g.stroke();
    }
  } else if (type === "gas") {
    const n = 9 + Math.floor(R(5));
    for (let i = 0; i < n; i++) {
      const y = (i / n) * res, h = res / n * (0.7 + R(0.8));
      g.fillStyle = shade(0.7 + R(0.7));
      g.globalAlpha = 0.55 + R(0.45);
      g.fillRect(0, y, res, h);
    }
    g.globalAlpha = 1;
    for (let i = 0; i < 90; i++) {
      const y = R(res), x = R(res), w = 8 + R(res * 0.25);
      g.strokeStyle = shade(0.6 + R(0.8)); g.lineWidth = 1 + R(2.5);
      g.globalAlpha = 0.25 + R(0.3);
      g.beginPath(); g.moveTo(x, y);
      for (let s = 0; s < 6; s++) g.lineTo(x + s * w / 6, y + (R(6) - 3));
      g.stroke();
    }
    g.globalAlpha = 1;
    if (def.spot) {
      g.fillStyle = "rgba(190,70,50,0.75)";
      g.beginPath(); g.ellipse(res * 0.72, res * 0.52, res * 0.075, res * 0.04, 0, 0, 7); g.fill();
      g.strokeStyle = "rgba(255,220,190,0.5)"; g.lineWidth = 2; g.stroke();
    }
  } else if (type === "venus") {
    for (let i = 0; i < 26; i++) {
      const y = (i / 26) * res, h = res / 26 * (0.6 + R(0.7));
      g.fillStyle = shade(0.8 + R(0.5));
      g.globalAlpha = 0.5 + R(0.5);
      g.fillRect(0, y, res, h);
    }
    g.globalAlpha = 1;
    for (let i = 0; i < 60; i++) {
      const y = R(res), x = R(res);
      g.fillStyle = shade(0.9 + R(0.3)); g.globalAlpha = 0.2 + R(0.2);
      g.beginPath(); g.arc(x, y, 4 + R(10), 0, 7); g.fill();
    }
    g.globalAlpha = 1;
  } else { /* rocky — mercury / mars */
    for (let i = 0; i < 2400; i++) {
      g.fillStyle = "rgba(0,0,0," + (0.10 + R(0.18)) + ")";
      g.fillRect(R(res), R(res), 1 + R(2.2), 1 + R(2.2));
      g.fillStyle = "rgba(255,255,255," + (0.05 + R(0.1)) + ")";
      g.fillRect(R(res), R(res), 1, 1);
    }
    for (let i = 0; i < 30; i++) {
      const x = R(res), y = R(res), r = 2 + R(res * 0.05);
      g.fillStyle = "rgba(0,0,0,0.35)"; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
      g.strokeStyle = "rgba(255,255,255,0.22)"; g.lineWidth = 1.5; g.stroke();
    }
  }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.generateMipmaps = false; t.minFilter = THREE.LinearFilter;   // no mipmap softening
  try { t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy()); } catch (e) {}
  return t;
}
function ringTexture() {
  const c = document.createElement("canvas"); c.width = c.height = 256;
  const g = c.getContext("2d");
  const R0 = 256 * 0.60, R1 = 256 * 0.985, n = 30;
  for (let i = 0; i < n; i++) {
    const f = i / (n - 1), r = R0 + (R1 - R0) * f;
    const a = 0.30 + 0.45 * Math.abs(Math.sin(f * 14 + 1)) + Math.random() * 0.15;
    g.strokeStyle = "rgba(222,200,158," + a.toFixed(3) + ")";
    g.lineWidth = 2.2 + Math.random() * 4.5;
    g.beginPath(); g.arc(128, 128, r, 0, 7); g.stroke();
  }
  g.strokeStyle = "rgba(0,0,0,0.55)"; g.lineWidth = 5;   // Cassini division gap
  g.beginPath(); g.arc(128, 128, R0 + (R1 - R0) * 0.45, 0, 7); g.stroke();
  const t = new THREE.CanvasTexture(c);
  t.anisotropy = 4;
  t.generateMipmaps = false; t.minFilter = THREE.LinearFilter;
  return t;
}
const saturnRingTex = ringTexture();

/* ------------------------------------------------------------------ */
/* 4. Lattice shaders & materials                                     */
/* ------------------------------------------------------------------ */
const VERT = `\nuniform float uTime;\nuniform vec3  uOffset;\nuniform vec4  uMasses[8];\nuniform vec4  uSpins[8];\nuniform float uMassCount;\nuniform float uN;\nuniform float uPhi0;\nuniform float uAlpha;\nuniform float uDistort;\nuniform float uWScale;\nuniform float uWFactor;\nuniform float uBreath;\nattribute float aVar;\nvarying float vVar;\nvarying float vMassA;\nvarying vec3  vWorld;\nvarying vec3  vViewN;\nvarying vec3  vViewDir;\nvarying float vViewZ;\n\nfloat thresh(float phi){\n  float x = pow(max(phi / uPhi0, 0.0), uN);\n  return x / (1.0 + x);\n}\n\nvoid main(){\n  vec4 w0 = instanceMatrix * vec4(position, 1.0);\n  vec3 wp = w0.xyz + uOffset;\n  /* pulsar frame-dragging swirl — shears the local fabric around the spin axis */\n  for (int i = 0; i < 8; i++){\n    if (float(i) >= uMassCount) break;\n    float sp = uSpins[i].w;\n    if (abs(sp) < 0.001) continue;\n    vec3 mp = uMasses[i].xyz;\n    float gm = uMasses[i].w;\n    if (gm < 0.0001) continue;\n    float r = length(wp - mp);\n    float phi = gm / max(r, 0.08);\n    float f = thresh(phi);\n    float fall = 1.0 / (1.0 + pow(r / 7.0, 4.0));\n    float A = uAlpha * f * fall;\n    float ang = A * sp * 0.30 / (1.0 + r * 0.3);\n    vec3 ax = normalize(uSpins[i].xyz);\n    vec3 rel = wp - mp;\n    float c = cos(ang), s = sin(ang);\n    wp = mp + rel * c + cross(ax, rel) * s + ax * dot(ax, rel) * (1.0 - c);\n  }\n  vec3 nrm = normalize(mat3(instanceMatrix) * normal);\n  vec3 disp = vec3(0.0);\n  float act = 0.0;\n  vec3 WD = normalize(vec3(1.0, 1.0, 1.0));      // projected 4th-spatial axis\n  for (int i = 0; i < 8; i++){\n    if (float(i) >= uMassCount) break;\n    vec3 mp = uMasses[i].xyz;\n    float gm = uMasses[i].w;\n    if (gm < 0.0001) continue;\n    vec3 d = wp - mp;\n    float r = length(d);\n    float phi = gm / max(r, 0.08);\n    float f = thresh(phi);\n    float fall = 1.0 / (1.0 + pow(r / 7.0, 4.0));\n    float A = uAlpha * f * fall;\n    act += A;\n    vec3 rd = d / max(r, 1e-4);\n    disp += rd * A * uDistort * 1.4;                             // radial pull\n    vec3 tv = normalize(cross(rd, vec3(0.2, 1.0, 0.3)) + vec3(1e-5));\n    disp += tv * A * uDistort * 0.7 * sin(length(wp) * 0.35 + uTime * 0.25);   // twist\n    vec3 tv2 = cross(rd, tv);\n    disp += tv2 * A * uDistort * 0.4 * cos(uTime * 0.4 + float(i));           // spiral\n    disp += WD * A * uWScale * uWFactor * 1.2;                   // W extrusion\n  }\n  vec3 sc = uOffset + (wp + disp - uOffset) * (1.0 + uBreath);\n  vWorld = sc;\n  vMassA = act;\n  vVar = aVar;\n  vec4 mv = viewMatrix * vec4(sc, 1.0);\n  vViewZ = -mv.z;\n  vViewDir = normalize(-mv.xyz);\n  vViewN = normalize(mat3(viewMatrix) * nrm);\n  gl_Position = projectionMatrix * mv;\n}\n`;

const FRAG = `\nuniform vec3  uColor;\nuniform vec3  uEmissive;\nuniform float uPulse;\nuniform float uIsW;\nuniform float uTime;\nuniform vec4  uMasses[8];\nuniform float uMassCount;\nuniform float uN;\nuniform float uPhi0;\nuniform float uAlpha;\nuniform float uFadeNear;\nuniform float uFadeFar;\nuniform vec3  uBg;\nvarying float vVar;\nvarying float vMassA;\nvarying vec3  vWorld;\nvarying vec3  vViewN;\nvarying vec3  vViewDir;\nvarying float vViewZ;\n\nfloat thresh(float phi){\n  float x = pow(max(phi / uPhi0, 0.0), uN);\n  return x / (1.0 + x);\n}\n\nvoid main(){\n  vec3 N = normalize(vViewN);\n  vec3 V = normalize(vViewDir);\n  vec3 L1 = normalize(vec3(0.45, 0.85, 0.35));    // key light, above-left\n  vec3 L2 = normalize(vec3(-0.4, -0.7, 0.3));     // soft fill from below\n  float key = max(dot(N, L1), 0.0);\n  float fill = max(dot(N, L2), 0.0) * 0.4;\n  float rim = pow(1.0 - abs(dot(N, V)), 2.0) * 0.55;\n  float lit = 0.60 + 0.40 * key + fill + rim;\n  vec3 col = uColor * (0.62 + 0.50 * vVar) * lit;\n  col += uEmissive * (0.22 + 1.15 * uPulse);\n  col *= 1.0 + 0.05 * sin(uTime * 0.8 + length(vWorld) * 3.0);\n  float A = 0.0;\n  for (int i = 0; i < 8; i++){\n    if (float(i) >= uMassCount) break;\n    vec3 mp = uMasses[i].xyz;\n    float gm = uMasses[i].w;\n    if (gm < 0.0001) continue;\n    float r = length(vWorld - mp);\n    float phi = gm / max(r, 0.08);\n    float f = thresh(phi);\n    float fall = 1.0 / (1.0 + pow(r / 7.0, 4.0));\n    A += f * fall;\n  }\n  col *= 1.0 + A * (0.3 + 2.4 * uIsW);            // red W-edges intensify near mass\n  float fade = smoothstep(uFadeFar, uFadeNear, vViewZ);\n  col = mix(uBg, col, fade);\n  gl_FragColor = vec4(col, 1.0);\n}\n`;

const MATDEFS = [
  { color: 0x12e58e, emis: 0x66ffc2, wf: 0.55, isW: 0, phase: 0.00 },   // emerald outer lattice
  { color: 0x2a5ff0, emis: 0x82a4ff, wf: 1.45, isW: 0, phase: 0.30 },   // sapphire mid-layers
  { color: 0x14c8ef, emis: 0xa2f6ff, wf: 1.05, isW: 0, phase: 0.50 },   // cyan innermost cores
  { color: 0xff2f55, emis: 0xff7f92, wf: 2.20, isW: 1, phase: 0.72 }    // crimson W-diagonals
];
const shared = {
  uTime: { value: 0 }, uOffset: { value: new THREE.Vector3() },
  uMasses: { value: [] }, uSpins: { value: [] }, uMassCount: { value: 0 },
  uN: { value: CONFIG.metric.n }, uPhi0: { value: CONFIG.metric.phi0 }, uAlpha: { value: CONFIG.metric.alpha },
  uDistort: { value: CONFIG.visual.distort }, uWScale: { value: CONFIG.visual.wScale },
  uBreath: { value: 0.004 }, uFadeNear: { value: CONFIG.visual.fade }, uFadeFar: { value: CONFIG.visual.fade + 8 },
  uBg: { value: new THREE.Color(0xffffff) }
};
for (let i = 0; i < CONFIG.lattice.MAXM; i++) { shared.uMasses.value.push(new THREE.Vector4(0, 0, 0, 0)); shared.uSpins.value.push(new THREE.Vector4(0, 1, 0, 0)); }

const latticeMats = MATDEFS.map((d, i) => {
  const m = new THREE.ShaderMaterial({
    uniforms: Object.assign({}, {
      uColor: { value: new THREE.Color(d.color) },
      uEmissive: { value: new THREE.Color(d.emis) },
      uPulse: { value: 0 }, uIsW: { value: d.isW }, uWFactor: { value: d.wf }
    }, shared),
    vertexShader: VERT, fragmentShader: FRAG,
    transparent: false, depthWrite: true
  });
  m.userData.phase = d.phase;
  return m;
});

/* --- 2D-3D grid-sheet projection (gravity-well view) -----------------------
   The same fabric, rendered as a continuous paraboloid sheet instead of cubes.
   A second (cyan) sheet is displaced along the projected W axis; its
   separation from the emerald sheet equals the local size of the extra
   dimension D(r)/ℓ² — so the "thickness of 4D space" is directly visible.
   Crimson connector lines tie the two sheets wherever the threshold opens. */
const SHEET_VERT = `\nuniform float uTime;\nuniform vec3  uOffset;\nuniform vec4  uMasses[8];\nuniform vec4  uSpins[8];\nuniform float uMassCount;\nuniform float uN;\nuniform float uPhi0;\nuniform float uAlpha;\nuniform float uDistort;\nuniform float uWScale;\nuniform float uWellDepth;\nuniform float uWShift;\nuniform float uBreath;\nattribute float aVar;\nattribute float aW;\nvarying float vVar;\nvarying float vMassA;\nvarying vec3  vWorld;\nvarying float vViewZ;\n\nfloat thresh(float phi){\n  float x = pow(max(phi / uPhi0, 0.0), uN);\n  return x / (1.0 + x);\n}\n\nvoid main(){\n  vec3 wp = position + uOffset;\n  /* pulsar frame-dragging swirl in the sheet plane */\n  for (int i = 0; i < 8; i++){\n    if (float(i) >= uMassCount) break;\n    float sp = uSpins[i].w;\n    if (abs(sp) < 0.001) continue;\n    vec3 mp = uMasses[i].xyz;\n    float gm = uMasses[i].w;\n    if (gm < 0.0001) continue;\n    float r = length(wp - mp);\n    float phi = gm / max(r, 0.08);\n    float f = thresh(phi);\n    float fall = 1.0 / (1.0 + pow(r / 8.0, 4.0));\n    float A = uAlpha * f * fall;\n    float ang = A * sp * 0.30 / (1.0 + r * 0.3);\n    vec3 ax = normalize(uSpins[i].xyz);\n    vec3 rel = wp - mp;\n    float c = cos(ang), s = sin(ang);\n    wp = mp + rel * c + cross(ax, rel) * s + ax * dot(ax, rel) * (1.0 - c);\n  }\n  float act = 0.0, well = 0.0, sep = 0.0;\n  vec2  pull = vec2(0.0);\n  vec3 WD = normalize(vec3(1.0, 0.55, 1.0));            // projected 4th-spatial axis\n  for (int i = 0; i < 8; i++){\n    if (float(i) >= uMassCount) break;\n    vec3 mp = uMasses[i].xyz;\n    float gm = uMasses[i].w;\n    if (gm < 0.0001) continue;\n    vec2 d2 = wp.xz - mp.xz;\n    float r = length(d2);\n    float phi = gm / max(r, 0.08);\n    float f = thresh(phi);\n    float fall = 1.0 / (1.0 + pow(r / 8.0, 4.0));\n    float A = uAlpha * f * fall;\n    act += A;\n    well += f * fall * (1.0 / (1.0 + pow(r / 3.0, 2.0)));  // smooth Lorentzian well\n    sep += A;\n    pull += -d2 / max(r, 0.3) * A * 1.15;               // radial compression toward the mass\n  }\n  float ws = min(1.0, aW + uWShift);\n  vec3 disp = vec3(0.0);\n  disp.y -= well * uWellDepth * uDistort * 5.5;         // deep cinematic rubber-sheet well\n  disp.xz += pull * uWellDepth * uDistort * 1.3;        // grid flows inward, denser near the mass\n  disp += WD * sep * uWScale * 3.0 * ws;                // W-dimension sheet separation\n  vec3 sc = uOffset + (wp + disp - uOffset) * (1.0 + uBreath);\n  vWorld = sc;\n  vMassA = act;\n  vVar = aVar;\n  vec4 mv = viewMatrix * vec4(sc, 1.0);\n  vViewZ = -mv.z;\n  gl_Position = projectionMatrix * mv;\n}\n`;
const SHEET_FRAG = `\nuniform vec3  uColor;\nuniform vec3  uEmissive;\nuniform float uPulse;\nuniform float uIsW;\nuniform float uTime;\nuniform vec4  uMasses[8];\nuniform float uMassCount;\nuniform float uN;\nuniform float uPhi0;\nuniform vec3  uOffset;\nuniform float uGridR;\nuniform float uOpacity;\nuniform vec3  uBg;\nvarying float vVar;\nvarying float vMassA;\nvarying vec3  vWorld;\n\nfloat thresh(float phi){\n  float x = pow(max(phi / uPhi0, 0.0), uN);\n  return x / (1.0 + x);\n}\n\nvoid main(){\n  vec3 col = uColor * (0.90 + 0.45 * vVar);\n  col += uEmissive * (0.35 + 1.4 * uPulse);\n  col *= 1.0 + 0.05 * sin(uTime * 0.8 + length(vWorld) * 3.0);\n  float A = 0.0;\n  for (int i = 0; i < 8; i++){\n    if (float(i) >= uMassCount) break;\n    vec3 mp = uMasses[i].xyz;\n    float gm = uMasses[i].w;\n    if (gm < 0.0001) continue;\n    float r = length(vWorld - mp);\n    float phi = gm / max(r, 0.08);\n    float f = thresh(phi);\n    float fall = 1.0 / (1.0 + pow(r / 8.0, 4.0));\n    A += f * fall;\n  }\n  col *= 1.0 + A * (0.3 + 2.4 * uIsW);\n  /* dissolve into the void at the sheet's horizon instead of fading by camera distance */\n  float rad = length(vWorld.xz - uOffset.xz);\n  float fade = smoothstep(uGridR, uGridR - 9.0, rad);\n  col = mix(uBg, col, fade);\n  gl_FragColor = vec4(col, uOpacity);\n}\n`;
function sheetMaterial(srcMat, vertShader, opacity, color, emissive) {
  const unis = {};
  for (const k in srcMat.uniforms) unis[k] = srcMat.uniforms[k];   // share uniform objects
  unis.uColor = { value: new THREE.Color(color) };                 // fresh copies — sheet palette is independent
  unis.uEmissive = { value: new THREE.Color(emissive) };
  unis.uWShift = { value: 0 };
  unis.uWellDepth = { value: CONFIG.visual.wellDepth };
  unis.uGridR = { value: 1 };
  unis.uOpacity = { value: opacity };
  const m = new THREE.ShaderMaterial({ uniforms: unis, vertexShader: vertShader, fragmentShader: SHEET_FRAG, transparent: opacity < 1, depthWrite: opacity >= 1 });
  m.userData.phase = srcMat.userData.phase;
  return m;
}
/* 2D-3D grid-sheet palette — pure emerald-green glow on pitch black, so the
   X/Z fabric grid and the W-dimension separation read clearly (per the spec). */
const sheetMats = [
  sheetMaterial(latticeMats[0], SHEET_VERT, 1.0, 0x1fe98e, 0x7dffc8),  // fabric sheet (X/Z grid)
  sheetMaterial(latticeMats[2], SHEET_VERT, 0.42, 0x14d67c, 0x6effb6), // W-dimension ghost sheet
  sheetMaterial(latticeMats[3], SHEET_VERT, 1.0, 0x2bff9e, 0xa0ffd4)   // W-connectors
];
sheetMats[1].uniforms.uWShift.value = 1;

const fabricMats = [...latticeMats, ...sheetMats];
const sharedAll = () => { for (const m of fabricMats) for (const k in shared) m.uniforms[k].value = shared[k].value; };

const latticeContainer = new THREE.Group();
scene.add(latticeContainer);
const sheetGroup = new THREE.Group();
scene.add(sheetGroup);

sharedAll();
applyBg(CONFIG.visual.bg);

/* ------------------------------------------------------------------ */
/* 5. Lattice geometry & instanced build                              */
/* ------------------------------------------------------------------ */
const L = CONFIG.lattice.L, N = CONFIG.lattice.N, HALF = Math.floor(N / 2);
const IDQ = new THREE.Quaternion();
const ONE = new THREE.Vector3(1, 1, 1);
const YAX = new THREE.Vector3(0, 1, 0);

function hash3(a, b, c) {
  let h = (a | 0) * 73856093 ^ (b | 0) * 19349663 ^ (c | 0) * 83492791;
  h = (h ^ (h >>> 13)) * 1274126177; h = h ^ (h >>> 16);
  return ((h >>> 0) % 100000) / 100000;
}

const LEVELS = () => {
  const base = [
    { s: 1.00, mat: 0, rad: 0.042 },
    { s: 0.45, mat: 1, rad: 0.024 },
    { s: 0.225, mat: 2, rad: 0.014 }
  ];
  if (CONFIG.visual.deepNest) base.push({ s: 0.11, mat: 2, rad: 0.010 });
  return base;
};

const edgeGeos = [];       // [level][axis]
function buildGeometries() {
  for (const [li, lv] of LEVELS().entries()) {
    edgeGeos[li] = {};
    for (const axis of ["x", "y", "z"]) {
      const g = new THREE.CylinderGeometry(lv.rad, lv.rad, lv.s * L, 6, 1);
      if (axis === "x") g.rotateZ(Math.PI / 2);
      else if (axis === "z") g.rotateX(Math.PI / 2);
      edgeGeos[li][axis] = g;
    }
  }
}
const geoConn = new THREE.CylinderGeometry(0.016, 0.016, (0.8 - 0.18) * Math.sqrt(3), 6, 1);
const geoDiag = new THREE.CylinderGeometry(0.019, 0.019, L * Math.sqrt(3), 6, 1);
const qDirs = [];
for (let d = 0; d < 8; d++) {
  const dx = ((d >> 2) & 1) ? 1 : -1, dy = ((d >> 1) & 1) ? 1 : -1, dz = (d & 1) ? 1 : -1;
  qDirs.push(new THREE.Quaternion().setFromUnitVectors(YAX, new THREE.Vector3(dx, dy, dz).normalize()));
}

let latticeMeshes = [];
function buildLattice() {
  for (const m of latticeMeshes) { latticeContainer.remove(m); m.geometry.dispose(); }
  latticeMeshes = [];
  buildGeometries();

  const nodes = [];
  for (let i = -HALF; i <= HALF; i++) for (let j = -HALF; j <= HALF; j++) for (let k = -HALF; k <= HALF; k++)
    if (hash3(i, j, k) < CONFIG.visual.density) nodes.push([i, j, k]);
  const NC = nodes.length;

  const m4 = new THREE.Matrix4(), v3 = new THREE.Vector3();
  const varAttr = (mesh, count, seed) => {
    const a = new Float32Array(count);
    for (let i = 0; i < count; i++) a[i] = 0.82 + 0.36 * hash3(i * 7 + seed, i, seed + 3);
    mesh.geometry.setAttribute("aVar", new THREE.InstancedBufferAttribute(a, 1));
  };
  const add = (geo, mat, count, fill) => {
    const mesh = new THREE.InstancedMesh(geo, mat, count);
    let idx = 0;
    fill((pos, quat, seed) => { v3.copy(pos); m4.compose(v3, quat || IDQ, ONE); mesh.setMatrixAt(idx, m4); idx++; });
    mesh.count = count; mesh.instanceMatrix.needsUpdate = true;
    varAttr(mesh, count, idx);
    mesh.frustumCulled = false;
    latticeContainer.add(mesh); latticeMeshes.push(mesh);
    return mesh;
  };

  for (const [li, lv] of LEVELS().entries()) {
    const mat = latticeMats[lv.mat], s = lv.s * L;
    const offs = {
      x: [[0, s / 2, s / 2], [0, -s / 2, s / 2], [0, s / 2, -s / 2], [0, -s / 2, -s / 2]],
      y: [[s / 2, 0, s / 2], [-s / 2, 0, s / 2], [s / 2, 0, -s / 2], [-s / 2, 0, -s / 2]],
      z: [[s / 2, s / 2, 0], [-s / 2, s / 2, 0], [s / 2, -s / 2, 0], [-s / 2, -s / 2, 0]]
    };
    for (const axis of ["x", "y", "z"]) {
      add(edgeGeos[li][axis], mat, NC * 4, (set) => {
        for (const [i, j, k] of nodes)
          for (const [ox, oy, oz] of offs[axis])
            set(new THREE.Vector3(i * L + ox, j * L + oy, k * L + oz), null, 0);
      });
    }
  }

  const rMat = latticeMats[3];
  add(geoConn, rMat, NC * 8, (set) => {
    for (const [i, j, k] of nodes)
      for (let d = 0; d < 8; d++) {
        const dx = ((d >> 2) & 1) ? 1 : -1, dy = ((d >> 1) & 1) ? 1 : -1, dz = (d & 1) ? 1 : -1;
        set(new THREE.Vector3(i * L + dx * 0.49, j * L + dy * 0.49, k * L + dz * 0.49), qDirs[d], d + 1);
      }
  });
  const diagNodes = nodes.filter(([i, j, k]) => hash3(i + 31, j + 7, k + 13) < 0.3);
  add(geoDiag, rMat, diagNodes.length * 4, (set) => {
    for (const [i, j, k] of diagNodes)
      for (const d of [0, 3, 5, 6])
        set(new THREE.Vector3(i * L, j * L, k * L), qDirs[d], d + 2);
  });

  CONFIG._instances = latticeMeshes.reduce((a, m) => a + m.count, 0);
}
buildLattice();

/* --- grid-sheet build --- */
const GRID_SPAN = 26;   // cells per side; cell = L so the periodic recenter stays seamless
function buildSheet() {
  sheetGroup.clear();
  const g = L, linePos = [];
  for (let i = -GRID_SPAN; i <= GRID_SPAN; i++)
    for (let j = -GRID_SPAN; j < GRID_SPAN; j++) {
      linePos.push(i * g, 0, j * g, i * g, 0, (j + 1) * g);
      linePos.push(j * g, 0, i * g, (j + 1) * g, 0, i * g);
    }
  const connPos = [];
  for (let i = -GRID_SPAN; i <= GRID_SPAN; i++) for (let j = -GRID_SPAN; j <= GRID_SPAN; j++)
    connPos.push(i * g, 0, j * g, i * g, 0, j * g);
  const mk = (mat, arr) => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(new Float32Array(arr), 3));
    const n = arr.length / 3, av = new Float32Array(n), aw = new Float32Array(n);
    for (let i = 0; i < n; i++) av[i] = 0.82 + 0.36 * hash3(i * 13, i, 7);
    geo.setAttribute("aVar", new THREE.BufferAttribute(av, 1));
    geo.setAttribute("aW", new THREE.BufferAttribute(aw, 1));
    const line = new THREE.LineSegments(geo, mat);
    line.frustumCulled = false;
    return line;
  };
  const sheetA = mk(sheetMats[0], linePos);
  const sheetB = mk(sheetMats[1], linePos);
  const conn = mk(sheetMats[2], connPos);
  const aw = conn.geometry.attributes.aW.array;
  for (let i = 0; i < aw.length; i++) aw[i] = (i % 2);   // alternate: sheet A / sheet B
  conn.geometry.attributes.aW.needsUpdate = true;
  sheetGroup.add(sheetA, sheetB, conn);
  CONFIG._grid = { verts: (GRID_SPAN * 2 + 1) ** 2, segs: linePos.length / 6 + connPos.length / 6 };
}
buildSheet();

const GREEN5D = { color: 0x1fe98e, emis: 0x7dffc8 };
function setView(v) {
  CONFIG.visual.view = v;
  latticeContainer.visible = v === "cubic" || v === "5d";
  sheetGroup.visible = v === "sheet";
  /* 5D View: every layer of the lattice — nested cubes AND the W diagonals —
     renders in pure emerald green on pitch black. Colours are restored on exit. */
  for (const m of latticeMats) {
    if (v === "5d") {
      if (!m.userData.savedColor) {
        m.userData.savedColor = m.uniforms.uColor.value.clone();
        m.userData.savedEmis = m.uniforms.uEmissive.value.clone();
      }
      m.uniforms.uColor.value.setHex(GREEN5D.color);
      m.uniforms.uEmissive.value.setHex(GREEN5D.emis);
    } else if (m.userData.savedColor) {
      m.uniforms.uColor.value.copy(m.userData.savedColor);
      m.uniforms.uEmissive.value.copy(m.userData.savedEmis);
      m.userData.savedColor = null; m.userData.savedEmis = null;
    }
  }
  document.querySelectorAll("#viewSeg .segbtn").forEach(b => b.classList.toggle("on", b.dataset.view === v));
  /* the sheet and 5D views live on a pitch-black void; other views follow the background dropdown */
  applyBg(v === "sheet" || v === "5d" ? "dark" : CONFIG.visual.bg);
}
setView(CONFIG.visual.view);

const latticeCenter = new THREE.Vector3();
function recenterLattice() {
  const offX = camera.position.x - latticeCenter.x, offY = camera.position.y - latticeCenter.y, offZ = camera.position.z - latticeCenter.z;
  const th = L * (HALF - 2);
  let dx = 0, dy = 0, dz = 0;
  if (offX > th) dx = L * Math.ceil((offX - th) / L); else if (offX < -th) dx = L * Math.floor((offX + th) / L);
  if (offY > th) dy = L * Math.ceil((offY - th) / L); else if (offY < -th) dy = L * Math.floor((offY + th) / L);
  if (offZ > th) dz = L * Math.ceil((offZ - th) / L); else if (offZ < -th) dz = L * Math.floor((offZ + th) / L);
  if (dx || dy || dz) { latticeCenter.add(new THREE.Vector3(dx, dy, dz)); shared.uOffset.value.copy(latticeCenter); }
}

/* ------------------------------------------------------------------ */
/* 6. Physics engine — 5D effective potential                         */
/* ------------------------------------------------------------------ */
const EPS = 0.06, C_LIGHT = 1.35;
const majorBodies = [], ghosts = [], planets = [], meteors = [], beams = [];
/* cached dynamic-body list — rebuilt once per frame, reused by every integrator */
let DYN = [];
const _d = new THREE.Vector3();
function refreshDynBodies() {
  DYN.length = 0;
  for (const b of majorBodies) {
    const s = b.strength * b.decay;
    if (s < 0.001) continue;
    let pulse = 1;
    if (b.pulse) pulse = 1 + 0.35 * Math.sin(b.spinAngle * 4);
    DYN.push({ pos: b.anchor, GM: b.GM * s, warpGM: b.warpGM * s * pulse });
  }
  for (const p of planets) DYN.push({ pos: p.worldPos, GM: p.gm, warpGM: 0 });
  for (const m of meteors) DYN.push({ pos: m.worldPos, GM: m.gm, warpGM: 0 });   // meteors pull on each other too
}

function deltaEff(warpGM, r) {
  const x = Math.max(warpGM / Math.max(r, 0.15) / CONFIG.metric.phi0, 0);
  const f = Math.pow(x, CONFIG.metric.n) / (1 + Math.pow(x, CONFIG.metric.n));
  return 0.9 * CONFIG.metric.alpha * f;
}
function accAt(pos, out) {
  out.set(0, 0, 0);
  for (const b of DYN) {
    _d.subVectors(b.pos, pos);
    const r2 = _d.lengthSq() + EPS * EPS, r = Math.sqrt(r2);
    const dlt = deltaEff(b.warpGM, r);
    const a = b.GM * (1 + dlt) / (r2 * r);
    out.x += _d.x * a; out.y += _d.y * a; out.z += _d.z * a;
  }
  return out;
}
const _a = new THREE.Vector3();
function stepPhoton(p, v, dt) {
  accAt(p, _a);
  const vd = v.dot(_a);
  _a.x -= v.x * vd / (C_LIGHT * C_LIGHT); _a.y -= v.y * vd / (C_LIGHT * C_LIGHT); _a.z -= v.z * vd / (C_LIGHT * C_LIGHT);
  v.addScaledVector(_a, dt);
  v.setLength(C_LIGHT);
  p.addScaledVector(v, dt);
}
function stepBody(p, v, dt) {
  accAt(p, _a);
  v.addScaledVector(_a, dt);
  p.addScaledVector(v, dt);
}

function syncMassUniforms() {
  const src = [];
  for (const b of majorBodies) {
    const s = b.strength * b.decay;
    if (s < 0.001) continue;
    let pulse = 1;
    if (b.pulse) pulse = 1 + 0.35 * Math.sin(b.spinAngle * 4);
    src.push({ pos: b.anchor, gm: b.warpGM * s * pulse * CONFIG.visual.warpMul, spin: b.spin ? b.spinAngle : 0 });
  }
  for (const g of ghosts) if (g.decay > 0.02) src.push({ pos: g.pos, gm: g.gm * g.decay * CONFIG.visual.warpMul, spin: 0 });
  src.sort((a, b) => b.gm - a.gm);
  const n = Math.min(CONFIG.lattice.MAXM, src.length);
  for (let i = 0; i < CONFIG.lattice.MAXM; i++) {
    const s = src[i];
    const v = shared.uMasses.value[i];
    const sv = shared.uSpins.value[i];
    if (s) { v.set(s.pos.x, s.pos.y, s.pos.z, s.gm); sv.set(0, 1, 0, s.spin); }
    else { v.set(0, 0, 0, 0); sv.set(0, 0, 0, 0); }
  }
  shared.uMassCount.value = n;
}

/* well depth at a world (x, z) — must match the sheet vertex shader exactly */
function wellAt(x, z) {
  let w = 0;
  for (const b of majorBodies) {
    const s = b.strength * b.decay * CONFIG.visual.warpMul;
    if (s < 0.0001) continue;
    let pulse = 1;
    if (b.pulse) pulse = 1 + 0.35 * Math.sin(b.spinAngle * 4);
    const gm = b.warpGM * s * pulse;
    const r = Math.hypot(x - b.anchor.x, z - b.anchor.z);
    const phi = gm / Math.max(r, 0.08);
    const xr = Math.pow(phi / CONFIG.metric.phi0, CONFIG.metric.n);
    const f = xr / (1 + xr);
    const fall = 1 / (1 + Math.pow(r / 8, 4));
    const g = 1 / (1 + Math.pow(r / 3, 2));
    w += f * fall * g;
  }
  return w * CONFIG.visual.wellDepth * CONFIG.visual.distort * 5.5;
}

/* ------------------------------------------------------------------ */
/* 7. Celestial bodies                                                */
/* ------------------------------------------------------------------ */
const pickables = [];
let selected = null;

function makeGlowSprite(tex, color, scale) {
  const mat = new THREE.SpriteMaterial({ map: tex, color: color, transparent: true, depthWrite: false, opacity: 0.85 });
  const sp = new THREE.Sprite(mat); sp.scale.setScalar(scale);
  return sp;
}
function makeTrail(color, len) {
  const pos = new Float32Array(len * 3);
  const col = new Float32Array(len * 3);
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  g.setAttribute("color", new THREE.BufferAttribute(col, 3));
  const m = new THREE.LineBasicMaterial({ color: color, vertexColors: true, transparent: true, opacity: 0.85, depthWrite: false });
  return { line: new THREE.Line(g, m), n: len, pos, col };
}
function updateTrail(t, pts) {
  for (let i = 0; i < t.n; i++) {
    const q = (t.n - 1 - i);
    const p = pts[Math.max(0, q)];
    if (!p) { t.pos[i * 3] = 0; t.pos[i * 3 + 1] = 0; t.pos[i * 3 + 2] = 0; t.col[i * 3] = 1; t.col[i * 3 + 1] = 1; t.col[i * 3 + 2] = 1; continue; }
    t.pos[i * 3] = p.x; t.pos[i * 3 + 1] = p.y; t.pos[i * 3 + 2] = p.z;
    const f = i / t.n;
    const base = t.line.material.color;
    t.col[i * 3] = base.r + (1 - base.r) * f; t.col[i * 3 + 1] = base.g + (1 - base.g) * f; t.col[i * 3 + 2] = base.b + (1 - base.b) * f;
  }
  t.line.geometry.attributes.position.needsUpdate = true;
  t.line.geometry.attributes.color.needsUpdate = true;
}

/* ---- Solar system ---- */
const PLANET_DEFS = [
  { name: "Mercury", r: 2.0, size: 0.13, color: 0xb9a38a, gm: 0.0002, tex: "rocky", tilt: 0.03, spin: 2.6 },
  { name: "Venus",   r: 2.6, size: 0.21, color: 0xe0b878, gm: 0.0005, tex: "venus", tilt: 0.06, spin: 0.7 },
  { name: "Earth",   r: 3.3, size: 0.23, color: 0x4f9df7, gm: 0.0006, tex: "earth", tilt: 0.41, spin: 1.5 },
  { name: "Mars",    r: 4.0, size: 0.17, color: 0xd1644a, gm: 0.0001, tex: "rocky", tilt: 0.44, spin: 1.4 },
  { name: "Jupiter", r: 5.1, size: 0.52, color: 0xd8b98a, gm: 0.012, tex: "gas", spot: true, tilt: 0.05, spin: 3.0 },
  { name: "Saturn",  r: 6.2, size: 0.44, color: 0xe6cf9e, gm: 0.009, tex: "gas", ring: true, tilt: 0.47, spin: 2.7 },
  { name: "Uranus",  r: 7.2, size: 0.29, color: 0x9fd8e8, gm: 0.004, tex: "gas", tilt: 1.65, spin: 1.1 },
  { name: "Neptune", r: 8.1, size: 0.27, color: 0x4f7fe0, gm: 0.0048, tex: "gas", spot: true, tilt: 0.49, spin: 1.3 }
];
function applyPlanetDetail() {
  for (const p of planets) {
    const seg = Math.max(20, Math.round(30 * CONFIG.camera.planetDetail));
    const res = Math.max(96, Math.round(192 * CONFIG.camera.planetDetail));
    p.mesh.geometry.dispose();
    p.mesh.geometry = new THREE.SphereGeometry(p.def.size, seg, Math.round(seg * 0.7));
    if (p.mat.map) p.mat.map.dispose();
    p.tex = planetTexture(p.def, res);
    p.mat.map = p.tex;
    p.mat.needsUpdate = true;
  }
}
const SUN_GM = 1.2, SUN_WARP = 2.5e-6;   // physical solar compactness GM/c²R ≈ 2.5e-6 → Δ ~ 10⁻³³ (spec's 10⁻²⁸–10⁻³⁴ band)
function addSolarSystem(pos) {
  if (majorBodies.length >= CONFIG.bodies.maxMajor) return;
  const group = new THREE.Group(); group.position.copy(pos);
  const sunMesh = new THREE.Mesh(new THREE.SphereGeometry(0.55, 48, 36), new THREE.MeshBasicMaterial({ map: sunTexture() }));
  group.add(sunMesh);
  group.add(makeGlowSprite(glowOran, 0xffcf7a, 3.4));
  const corona = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowOran, color: 0xffcf7a, transparent: true, opacity: 0.28, depthWrite: false }));
  corona.scale.setScalar(7.5); group.add(corona);
  const orbitMats = [];
  const sys = { group, sunMesh, planets: [] };
  for (const pd of PLANET_DEFS) {
    /* high-detail textured planet: segment count and texture resolution follow
       the Planet detail slider, so quality is controllable up to crisp close-ups */
    const seg = Math.max(20, Math.round(30 * CONFIG.camera.planetDetail));
    const res = Math.max(96, Math.round(192 * CONFIG.camera.planetDetail));
    const tex = planetTexture(pd, res);
    const mat = new THREE.MeshStandardMaterial({ map: tex, roughness: 0.92, metalness: 0.02 });
    const pm = new THREE.Mesh(new THREE.SphereGeometry(pd.size, seg, Math.round(seg * 0.7)), mat);
    pm.position.set(pd.r, 0, 0);
    pm.rotation.z = pd.tilt || 0;                       // axial tilt
    pm.rotation.y = Math.random() * Math.PI * 2;        // random longitude
    if (pd.ring) {
      const rg = new THREE.RingGeometry(pd.size * 1.5, pd.size * 2.4, 56);
      const rmesh = new THREE.Mesh(rg, new THREE.MeshBasicMaterial({ map: saturnRingTex, side: THREE.DoubleSide, transparent: true, opacity: 0.85, depthWrite: false }));
      rmesh.rotation.x = Math.PI / 2.3;
      pm.add(rmesh);
    }
    const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowWhite, color: pd.color, transparent: true, depthWrite: false, opacity: 0.22 }));
    halo.scale.setScalar(pd.size * 3.6);
    pm.add(halo);
    group.add(pm);
    const trail = makeTrail(pd.color, 46); scene.add(trail.line);
    const oc = new THREE.Line(new THREE.BufferGeometry().setFromPoints(
      Array.from({ length: 65 }, (_, i) => { const a = i / 65 * Math.PI * 2; return new THREE.Vector3(Math.cos(a) * pd.r, 0, Math.sin(a) * pd.r); })),
      new THREE.LineBasicMaterial({ color: 0xc9d6ee, transparent: true, opacity: 0.35, depthWrite: false }));
    /* the guide circle is already generated in the XZ plane — no rotation, so all
       orbits stay horizontal exactly as the planets and meteors travel */
    group.add(oc);
    const worldPos = new THREE.Vector3(pos.x + pd.r, pos.y, pos.z);
    const theta = Math.random() * Math.PI * 2;
    worldPos.set(pos.x + pd.r * Math.cos(theta), pos.y, pos.z + pd.r * Math.sin(theta));
    const v0 = Math.sqrt(SUN_GM / pd.r);
    const vel = new THREE.Vector3(-Math.sin(theta) * v0, 0, Math.cos(theta) * v0);
    const p = { def: pd, mesh: pm, mat, tex, worldPos, vel, gm: pd.gm, trail, hist: [], system: sys,
      spinSpeed: (pd.spin || 1) * 0.08 + 0.05 };
    planets.push(p); sys.planets.push(p); pickables.push(pm); pm.userData.body = p;
  }
  scene.add(group);
  const body = { type: "sun", name: "Solar System", group, anchor: pos.clone(), GM: SUN_GM, warpGM: SUN_WARP, strength: 1, decay: 1, pulse: false, spinAngle: 0, sys };
  majorBodies.push(body); pickables.push(sunMesh); sunMesh.userData.body = body;
  syncMassUniforms();
  return body;
}

/* ---- Single Sun (weak-field safe) ---- */
function addSun(pos) {
  if (majorBodies.length >= CONFIG.bodies.maxMajor) return;
  const group = new THREE.Group(); group.position.copy(pos);
  const sunMesh = new THREE.Mesh(new THREE.SphereGeometry(0.55, 48, 36), new THREE.MeshBasicMaterial({ map: sunTexture() }));
  group.add(sunMesh);
  group.add(makeGlowSprite(glowOran, 0xffcf7a, 3.4));
  const corona = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowOran, color: 0xffcf7a, transparent: true, opacity: 0.28, depthWrite: false }));
  corona.scale.setScalar(7.5); group.add(corona);
  scene.add(group);
  const body = { type: "sun", name: "Sun", group, anchor: pos.clone(), GM: SUN_GM, warpGM: SUN_WARP, strength: 1, decay: 1, pulse: false, spinAngle: 0, core: sunMesh };
  majorBodies.push(body); pickables.push(sunMesh); sunMesh.userData.body = body;
  syncMassUniforms();
  return body;
}

/* ---- Heavy Star (intermediate threshold regime) ---- */
const HEAVY_GM = 2.6, HEAVY_WARP = 0.07;
function addHeavyStar(pos) {
  if (majorBodies.length >= CONFIG.bodies.maxMajor) return;
  const group = new THREE.Group(); group.position.copy(pos);
  /* hotter, brighter photosphere — whiter core than the Sun */
  const core = new THREE.Mesh(new THREE.SphereGeometry(0.72, 56, 42),
    new THREE.MeshBasicMaterial({ map: sunTexture("#ffffff", "#fff6d0", "#ffcf7a") }));
  group.add(core);
  group.add(makeGlowSprite(glowWhite, 0xfff6e0, 4.8));
  const corona = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowOran, color: 0xfff2cf, transparent: true, opacity: 0.3, depthWrite: false }));
  corona.scale.setScalar(9.5); group.add(corona);
  scene.add(group);
  const body = { type: "star", name: "Heavy Star", group, anchor: pos.clone(), GM: HEAVY_GM, warpGM: HEAVY_WARP, strength: 1, decay: 1, pulse: false, spinAngle: 0, core };
  majorBodies.push(body); pickables.push(core); core.userData.body = body;
  syncMassUniforms();
  return body;
}

/* ---- Black hole ---- */
const BH_GM = 1.8, BH_WARP = 2.0, BH_R = 0.55;
function addBlackHole(pos) {
  if (majorBodies.length >= CONFIG.bodies.maxMajor) return;
  const group = new THREE.Group(); group.position.copy(pos);
  const core = new THREE.Mesh(new THREE.SphereGeometry(BH_R, 32, 24), new THREE.MeshBasicMaterial({ color: 0x000000 }));
  group.add(core);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(BH_R * 1.55, 0.05, 8, 72), new THREE.MeshBasicMaterial({ color: 0xffb95e }));
  group.add(ring);
  const Np = 2400, diskPos = new Float32Array(Np * 3), diskCol = new Float32Array(Np * 3), diskData = [];
  const cIn = new THREE.Color(0xffd98a), cMid = new THREE.Color(0xff9d3c), cOut = new THREE.Color(0xff5a2a), cW = new THREE.Color(0xfff3d0);
  for (let i = 0; i < Np; i++) {
    const r = 1.1 + Math.random() * 1.6, a = Math.random() * Math.PI * 2, th = (Math.random() - 0.5) * 0.12;
    diskData.push({ r, a, th });
    const t = (r - 1.1) / 1.6, col = (t < 0.5 ? cIn.clone().lerp(cMid, t * 2) : cMid.clone().lerp(cOut, (t - 0.5) * 2)).lerp(cW, Math.random() * 0.25);
    diskCol[i * 3] = col.r; diskCol[i * 3 + 1] = col.g; diskCol[i * 3 + 2] = col.b;
  }
  const dg = new THREE.BufferGeometry();
  dg.setAttribute("position", new THREE.BufferAttribute(diskPos, 3));
  dg.setAttribute("color", new THREE.BufferAttribute(diskCol, 3));
  const disk = new THREE.Points(dg, new THREE.PointsMaterial({ size: 0.055, map: glowOran, vertexColors: true, transparent: true, depthWrite: false, sizeAttenuation: true }));
  disk.rotation.x = 0.35;
  group.add(disk);
  const jetGeo = new THREE.CylinderGeometry(0.02, 0.14, 4.6, 10, 1, true);
  const jetMat = new THREE.MeshBasicMaterial({ color: 0xbfe0ff, transparent: true, opacity: 0.5, depthWrite: false });
  const jet1 = new THREE.Mesh(jetGeo, jetMat); jet1.position.y = 2.4; group.add(jet1);
  const jet2 = new THREE.Mesh(jetGeo, jetMat); jet2.position.y = -2.4; jet2.rotation.x = Math.PI; group.add(jet2);
  const jN = 160, jPos = new Float32Array(jN * 3), jData = [];
  for (let i = 0; i < jN; i++) jData.push({ t: Math.random(), side: Math.random() < 0.5 ? 1 : -1, off: (Math.random() - 0.5) * 0.12 });
  const jg = new THREE.BufferGeometry(); jg.setAttribute("position", new THREE.BufferAttribute(jPos, 3));
  const jp = new THREE.Points(jg, new THREE.PointsMaterial({ size: 0.05, map: glowWhite, color: 0xd8ecff, transparent: true, depthWrite: false }));
  group.add(jp);
  scene.add(group);
  const body = { type: "bh", name: "Black Hole", group, anchor: pos.clone(), GM: BH_GM, warpGM: BH_WARP, strength: 1, decay: 1, pulse: false, spinAngle: 0, disk, diskData, jPos, jData };
  majorBodies.push(body); pickables.push(core); core.userData.body = body;
  syncMassUniforms();
  return body;
}

/* ---- Neutron star ---- */
const NS_GM = 0.5, NS_WARP = 0.55;
function addNeutronStar(pos) {
  if (majorBodies.length >= CONFIG.bodies.maxMajor) return;
  const group = new THREE.Group(); group.position.copy(pos);
  const core = new THREE.Mesh(new THREE.SphereGeometry(0.3, 28, 20), new THREE.MeshBasicMaterial({ color: 0xdff0ff }));
  group.add(core);
  group.add(makeGlowSprite(glowCyan, 0xcfe8ff, 1.9));
  const beamGeo = new THREE.CylinderGeometry(0.02, 0.13, 2.3, 10, 1, true);
  const beamMat = new THREE.MeshBasicMaterial({ color: 0xc9e8ff, transparent: true, opacity: 0.5, depthWrite: false });
  const b1 = new THREE.Mesh(beamGeo, beamMat); b1.position.y = 1.3; group.add(b1);
  const b2 = new THREE.Mesh(beamGeo, beamMat); b2.position.y = -1.3; b2.rotation.x = Math.PI; group.add(b2);
  for (let i = 0; i < 5; i++) {
    const fl = new THREE.Mesh(new THREE.TorusGeometry(0.95, 0.012, 4, 48),
      new THREE.MeshBasicMaterial({ color: 0x8fd0ff, transparent: true, opacity: 0.3, depthWrite: false }));
    fl.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
    group.add(fl);
  }
  scene.add(group);
  const body = { type: "ns", name: "Neutron Star", group, anchor: pos.clone(), GM: NS_GM, warpGM: NS_WARP, strength: 1, decay: 1, pulse: true, spinAngle: 0, core };
  majorBodies.push(body); pickables.push(core); core.userData.body = body;
  syncMassUniforms();
  return body;
}

/* ---- Pulsar ---- */
const PS_GM = 0.55, PS_WARP = 0.55;
function addPulsar(pos) {
  if (majorBodies.length >= CONFIG.bodies.maxMajor) return;
  const group = new THREE.Group(); group.position.copy(pos);
  const core = new THREE.Mesh(new THREE.SphereGeometry(0.26, 28, 20), new THREE.MeshBasicMaterial({ color: 0xeaf6ff }));
  group.add(core);
  group.add(makeGlowSprite(glowWhite, 0xffffff, 1.6));
  const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowCyan, color: 0xbfe6ff, transparent: true, opacity: 0.45, depthWrite: false }));
  halo.scale.setScalar(3.2); group.add(halo);
  /* lighthouse beams — tilted off the spin axis so they sweep around as the star spins */
  const beamGeo = new THREE.CylinderGeometry(0.015, 0.09, 4.8, 10, 1, true);
  const beamMat = new THREE.MeshBasicMaterial({ color: 0xd9f0ff, transparent: true, opacity: 0.5, depthWrite: false });
  const b1 = new THREE.Mesh(beamGeo, beamMat); b1.position.y = 2.5;
  const b2 = new THREE.Mesh(beamGeo, beamMat); b2.position.y = -2.5; b2.rotation.x = Math.PI;
  const tilt = new THREE.Group(); tilt.add(b1, b2); tilt.rotation.z = 0.5;
  group.add(tilt);
  for (let i = 0; i < 5; i++) {
    const fl = new THREE.Mesh(new THREE.TorusGeometry(0.75, 0.011, 4, 40),
      new THREE.MeshBasicMaterial({ color: 0xa5d8ff, transparent: true, opacity: 0.28, depthWrite: false }));
    fl.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, Math.random() * Math.PI);
    group.add(fl);
  }
  scene.add(group);
  const body = { type: "pulsar", name: "Pulsar", group, anchor: pos.clone(), GM: PS_GM, warpGM: PS_WARP, strength: 1, decay: 1, pulse: true, spin: true, spinAngle: 0, core, beamMat };
  majorBodies.push(body); pickables.push(core); core.userData.body = body;
  syncMassUniforms();
  return body;
}

/* ---- Meteor swarm ---- */
function addMeteorSwarm(pos) {
  if (meteors.length >= CONFIG.bodies.maxMeteors) return;
  const target = nearestMajor(pos);
  const n = Math.min(18, CONFIG.bodies.maxMeteors - meteors.length);
  for (let i = 0; i < n; i++) {
    const geo = new THREE.IcosahedronGeometry(1, 1);
    const pv = geo.attributes.position;
    for (let v = 0; v < pv.count; v++) {
      const j = 0.72 + 0.5 * Math.random();
      pv.setXYZ(v, pv.getX(v) * j, pv.getY(v) * j, pv.getZ(v) * j);
    }
    geo.computeVertexNormals();
    const tint = 0.62 + 0.42 * Math.random();
    const mat = new THREE.MeshStandardMaterial({ map: rockTex, color: new THREE.Color(tint, tint * 0.97, tint * 0.9), roughness: 0.95, metalness: 0.05 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.scale.setScalar(0.05 + Math.random() * 0.07);
    scene.add(mesh);
    const center = target ? target.group.position.clone() : pos;
    const a = 2.2 + Math.random() * 4.5, e = 0.05 + Math.random() * 0.5;
    const theta = Math.random() * Math.PI * 2, r = a * (1 - e * e) / (1 + e * Math.cos(theta));
    const inc = (Math.random() - 0.5) * 0.04, raan = Math.random() * Math.PI * 2;  // ~horizontal orbits
    const lp = new THREE.Vector3(Math.cos(theta) * r, 0, Math.sin(theta) * r);
    lp.applyAxisAngle(new THREE.Vector3(0, 0, 1), inc).applyAxisAngle(new THREE.Vector3(0, 1, 0), raan);
    const worldPos = lp.clone().add(center);
    const GMref = target ? target.GM : SUN_GM;
    const vMag = Math.sqrt(GMref * (2 / r - 1 / a));
    const tang = new THREE.Vector3(-Math.sin(theta), 0, Math.cos(theta)).applyAxisAngle(new THREE.Vector3(0, 0, 1), inc).applyAxisAngle(new THREE.Vector3(0, 1, 0), raan);
    const vel = tang.multiplyScalar(vMag * 0.98);
    const trail = makeTrail(0xffb36b, 24); scene.add(trail.line);
    const meta = {
      mesh, worldPos, vel, trail, hist: [],
      gm: 0.0002 + Math.random() * 0.0005,      // small but real mass — meteors attract each other
      rotAxis: new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize(),
      rotSpeed: 1.5 + Math.random() * 2.5
    };
    meteors.push(meta); pickables.push(mesh); mesh.userData.body = meta;
  }
}
function nearestMajor(pos) {
  let best = null, bd = 1e9;
  for (const b of majorBodies) { const d = b.anchor.distanceTo(pos); if (d < bd) { bd = d; best = b; } }
  return best;
}

/* ---- Light beams & ambient photons ---- */
function addLight(pos) {
  if (beams.length >= CONFIG.bodies.maxBeams) return;
  const axes = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
  const ax = axes[(Math.random() * axes.length) | 0];
  const line = new THREE.Line(new THREE.BufferGeometry(),
    new THREE.LineBasicMaterial({ color: 0xff5a80, transparent: true, opacity: 0.55, depthWrite: false }));
  const pts = new THREE.Points(new THREE.BufferGeometry(),
    new THREE.PointsMaterial({ size: 0.13, map: glowRed, color: 0xfff0f4, transparent: true, depthWrite: false }));
  scene.add(line, pts);
  beams.push({ pos: pos.clone(), dir: new THREE.Vector3(...ax), t: 0, life: 12, maxLife: 12, line, pts });
  // burst of ambient photons
  for (let i = 0; i < 20; i++) spawnAmbient(pos, true);
}

const AMBIENT_N = 150, aPhot = [];
const aPos = new Float32Array(AMBIENT_N * 3);
const aGeo = new THREE.BufferGeometry(); aGeo.setAttribute("position", new THREE.BufferAttribute(aPos, 3));
const aPts = new THREE.Points(aGeo, new THREE.PointsMaterial({ size: 0.075, map: glowCyan, color: 0xd9f4ff, transparent: true, depthWrite: false }));
scene.add(aPts);
function spawnAmbient(near, fromLight) {
  const i = Math.floor(Math.random() * AMBIENT_N);
  let p;
  if (near) p = near.clone(); else {
    const c = Math.floor(Math.random() * (HALF * 2 + 1)) - HALF;
    p = new THREE.Vector3(c * L + (Math.random() - 0.5) * L * 0.6, c * L, c * L);
  }
  const axes = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]];
  const ax = axes[(Math.random() * axes.length) | 0];
  aPhot[i] = { pos: p, vel: new THREE.Vector3(...ax).multiplyScalar(C_LIGHT * (fromLight ? 0.75 : 0.55 + Math.random() * 0.5)), life: 14 + Math.random() * 12, max: 26 };
}
for (let i = 0; i < AMBIENT_N; i++) spawnAmbient(null, false);

/* ------------------------------------------------------------------ */
/* 8. Camera control                                                  */
/* ------------------------------------------------------------------ */
const cam = { mode: "cinematic", yaw: 0.6, pitch: -0.18, roll: 0, cinT: 0, cinR: 9.0, cinRT: 9.0 };
const keys = {};
const _up = new THREE.Vector3(0, 1, 0), _fwd = new THREE.Vector3(), _right = new THREE.Vector3();

function updateCamera(dt) {
  if (cam.mode === "cinematic") {
    /* slow, smooth zoom: the wheel sets a target and the radius eases toward it */
    cam.cinR += (cam.cinRT - cam.cinR) * (1 - Math.exp(-dt * 1.5));   // slow, deliberate zoom
    const t = cam.cinT;
    const r = Math.max(4.5, cam.cinR + 5.0 * Math.sin(t * 0.05));
    const a = t * 0.12;
    const h = 1.6 * Math.sin(t * 0.09);
    const target = new THREE.Vector3(
      latticeCenter.x + r * Math.cos(a), latticeCenter.y + h, latticeCenter.z + r * Math.sin(a) * 1.15);
    camera.position.lerp(target, 1 - Math.exp(-dt * 1.8));
    const look = new THREE.Vector3(latticeCenter.x + 0.6 * Math.sin(t * 0.07), latticeCenter.y + 0.35 * Math.sin(t * 0.05), latticeCenter.z);
    camera.lookAt(look);
    camera.rotateZ(0.16 * Math.sin(t * 0.06));
    cam.cinT += dt * 0.55;
    // mouse drag nudge
    if (cam.drag) {
      const rot = new THREE.Matrix4().makeRotationAxis(_up, cam.dragDX * dt * 0.0012);
      camera.position.applyMatrix4(rot);
    }
  } else {
    const spd = (keys["Shift"] ? CONFIG.camera.flySpeed * 3 : CONFIG.camera.flySpeed) * dt;
    camera.getWorldDirection(_fwd); _right.crossVectors(_fwd, _up).normalize();
    const mv = new THREE.Vector3();
    if (keys["KeyW"]) mv.add(_fwd); if (keys["KeyS"]) mv.sub(_fwd);
    if (keys["KeyA"]) mv.sub(_right); if (keys["KeyD"]) mv.add(_right);
    if (keys["KeyR"]) mv.y += 1; if (keys["KeyF"]) mv.y -= 1;
    if (mv.lengthSq() > 0) camera.position.addScaledVector(mv.normalize(), spd);
    if (keys["KeyQ"]) cam.roll += dt * 1.3; if (keys["KeyE"]) cam.roll -= dt * 1.3;
    if (cam.pan) camera.position.addScaledVector(_right, -cam.panDX * 0.0065).addScaledVector(_up, cam.panDY * 0.0065);
    if (cam.look) { cam.yaw -= cam.lookDX * 0.0020; cam.pitch -= cam.lookDY * 0.0020; cam.pitch = Math.max(-1.55, Math.min(1.55, cam.pitch)); }
    camera.rotation.set(cam.pitch, cam.yaw, cam.roll, "YXZ");
  }
  recenterLattice();
  shared.uOffset.value.copy(latticeCenter);
}

/* ------------------------------------------------------------------ */
/* 9. Input                                                            */
/* ------------------------------------------------------------------ */
const raycaster = new THREE.Raycaster(), ndc = new THREE.Vector2();
let placing = null, placingType = null;
const reticle = new THREE.Mesh(new THREE.RingGeometry(0.24, 0.3, 40), new THREE.MeshBasicMaterial({ color: 0xff3355, transparent: true, opacity: 0.9, depthWrite: false, side: THREE.DoubleSide }));
reticle.visible = false; scene.add(reticle);
const selRing = new THREE.Mesh(new THREE.TorusGeometry(0.5, 0.02, 8, 48), new THREE.MeshBasicMaterial({ color: 0x2fe8a0, transparent: true, opacity: 0.8, depthWrite: false }));
selRing.visible = false; scene.add(selRing);

const pointer = { down: false, x: 0, y: 0, moved: false, ctrl: false };
const el = renderer.domElement;
el.addEventListener("pointerdown", (e) => {
  pointer.down = true; pointer.x = e.clientX; pointer.y = e.clientY; pointer.moved = false; pointer.ctrl = e.ctrlKey;
  el.setPointerCapture(e.pointerId);
});
el.addEventListener("pointermove", (e) => {
  if (!pointer.down) {
    if (placing && e.buttons === 0) { const p = aimPoint(e); if (p) { reticle.visible = true; reticle.position.copy(snapNode(p)); } }
    return;
  }
  const dx = e.clientX - pointer.x, dy = e.clientY - pointer.y;
  if (Math.abs(dx) + Math.abs(dy) > 5) pointer.moved = true;
  if (pointer.ctrl && selected && majorBodies.includes(selected)) {
    const pl = planeThrough(selected.group.position);
    const q = intersectPlane(e, pl);
    if (q) { selected.anchor.copy(snapNode(q)); }
  } else if (cam.mode === "free") {
    if (e.buttons === 1) { cam.look = true; cam.lookDX = dx; cam.lookDY = dy; }
    if (e.buttons === 2) { cam.pan = true; cam.panDX = dx; cam.panDY = dy; }
  } else {
    if (e.buttons === 1 && placing) { const p = aimPoint(e); if (p) reticle.position.copy(snapNode(p)); }
    else if (e.buttons === 1) { cam.drag = true; cam.dragDX = dx; cam.dragDY = dy; }
  }
  pointer.x = e.clientX; pointer.y = e.clientY;
});
el.addEventListener("pointerup", (e) => {
  const wasClick = pointer.down && !pointer.moved && e.button === 0;
  pointer.down = false; cam.look = false; cam.pan = false; cam.drag = false;
  if (wasClick) {
    if (placing) { const p = aimPoint(e); if (p) { placeObject(placingType, snapNode(p)); exitPlacement(); } }
    else pickAt(e);
  }
});
el.addEventListener("contextmenu", (e) => { e.preventDefault(); if (placing) exitPlacement(); });
window.addEventListener("keydown", (e) => {
  keys[e.code] = true;
  if (e.code === "Space") { e.preventDefault(); setCamMode(cam.mode === "cinematic" ? "free" : "cinematic"); }
  if (e.code === "KeyP") paused = !paused;
  if (e.code === "Escape") exitPlacement();
  if (e.code === "Enter" && placing) { placeObject(placingType, snapNode(aimPoint({ clientX: window.innerWidth / 2, clientY: window.innerHeight / 2 }))); exitPlacement(); }
});
window.addEventListener("keyup", (e) => keys[e.code] = false);
el.addEventListener("wheel", (e) => {
  e.preventDefault();
  const d = e.deltaY > 0 ? 1 : -1;
  if (cam.mode === "cinematic") { cam.cinRT = Math.max(4.5, Math.min(30, cam.cinRT + d * 0.18)); }  // ~60% slower zoom
  else { camera.getWorldDirection(_fwd); camera.position.addScaledVector(_fwd, d * CONFIG.camera.flySpeed * 0.06); }  // slow fly-through
}, { passive: false });

function aimPoint(e) {
  ndc.x = (e.clientX / window.innerWidth) * 2 - 1; ndc.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(ndc, camera);
  const pl = new THREE.Plane().setFromNormalAndCoplanarPoint(camera.getWorldDirection(new THREE.Vector3()), camera.position.clone().addScaledVector(camera.getWorldDirection(new THREE.Vector3()), 14));
  const hit = new THREE.Vector3();
  return raycaster.ray.intersectPlane(pl, hit) ? hit : null;
}
function planeThrough(p) {
  return new THREE.Plane().setFromNormalAndCoplanarPoint(camera.getWorldDirection(new THREE.Vector3()), p);
}
function intersectPlane(e, pl) {
  ndc.x = (e.clientX / window.innerWidth) * 2 - 1; ndc.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(ndc, camera);
  const hit = new THREE.Vector3();
  return raycaster.ray.intersectPlane(pl, hit) ? hit : null;
}
function snapNode(p) {
  return new THREE.Vector3(Math.round(p.x / L) * L, Math.round(p.y / L) * L, Math.round(p.z / L) * L);
}
function pickAt(e) {
  ndc.x = (e.clientX / window.innerWidth) * 2 - 1; ndc.y = -(e.clientY / window.innerHeight) * 2 + 1;
  raycaster.setFromCamera(ndc, camera);
  const hits = raycaster.intersectObjects(pickables, false);
  if (hits.length) select(hits[0].object.userData.body || null);
  else select(null);
}
function select(body) {
  selected = (body && (majorBodies.includes(body) || meteors.includes(body))) ? body : null;
  selRing.visible = !!selected;
  const card = document.getElementById("selCard");
  card.hidden = !selected;
  if (selected) {
    const isMajor = majorBodies.includes(selected);
    const sp = selected.anchor ? selected.anchor : (selected.group ? selected.group.position : selected.worldPos);
    document.getElementById("selInfo").textContent = (selected.name || "Meteor") + "  " +
      (isMajor ? "Δ " + readDelta(selected).toFixed(2) + "%" : "meteor") +
      "\npos " + sp.toArray().map(v => v.toFixed(1)).join(", ");
    document.getElementById("selStr").disabled = !isMajor;
    document.getElementById("selStrVal").textContent = (selected.strength || 1).toFixed(2) + "×";
    if (isMajor) document.getElementById("selStr").value = selected.strength;
  }
  refreshList();
}
function enterPlacement(type) {
  exitPlacement();
  placing = true; placingType = type;
  document.getElementById("banner").style.display = "block";
  document.getElementById("banner").innerHTML = "Placement mode — click in the scene to place, <code>Enter</code> for auto, <code>Esc</code> to cancel";
}
function exitPlacement() {
  placing = false; placingType = null; reticle.visible = false;
  document.getElementById("banner").style.display = "none";
}
function placeObject(type, p) {
  let b = null;
  if (type === "sys") b = addSolarSystem(p);
  else if (type === "sun") b = addSun(p);
  else if (type === "star") b = addHeavyStar(p);
  else if (type === "bh") b = addBlackHole(p);
  else if (type === "ns") b = addNeutronStar(p);
  else if (type === "pulsar") b = addPulsar(p);
  else if (type === "meteors") addMeteorSwarm(p);
  else if (type === "light") addLight(p);
  if (b) select(b);
  refreshList();
}

/* ------------------------------------------------------------------ */
/* 10. UI wiring                                                       */
/* ------------------------------------------------------------------ */
const $ = (id) => document.getElementById(id);
function bindSlider(id, vid, fmt, fn, init) {
  const el = $(id);
  el.addEventListener("input", () => { const v = parseFloat(el.value); if (vid) $(vid).textContent = fmt(v); fn(v); });
  if (init !== undefined) el.value = init;
}
bindSlider("sN", "vN", v => v.toFixed(1), v => CONFIG.metric.n = v, CONFIG.metric.n);
bindSlider("sPhi0", "vPhi0", v => v.toFixed(3), v => CONFIG.metric.phi0 = v, CONFIG.metric.phi0);
bindSlider("sAlpha", "vAlpha", v => v.toFixed(3), v => CONFIG.metric.alpha = v, CONFIG.metric.alpha);
bindSlider("sL", "vL", v => v.toFixed(1), v => CONFIG.metric.ell = v, CONFIG.metric.ell);
bindSlider("sWarp", "vWarp", v => v.toFixed(2) + "×", v => CONFIG.visual.warpMul = v, CONFIG.visual.warpMul);
bindSlider("sDist", "vDist", v => v.toFixed(2), v => CONFIG.visual.distort = v, CONFIG.visual.distort);
bindSlider("sWSc", "vWSc", v => v.toFixed(2), v => CONFIG.visual.wScale = v, CONFIG.visual.wScale);
bindSlider("sWell", "vWell", v => v.toFixed(2), v => CONFIG.visual.wellDepth = v, CONFIG.visual.wellDepth);
document.querySelectorAll("#viewSeg .segbtn").forEach(b => b.addEventListener("click", () => setView(b.dataset.view)));
bindSlider("sWave", "vWave", v => v.toFixed(2), v => CONFIG.visual.wave = v, CONFIG.visual.wave);
bindSlider("sBreath", "vBreath", v => v.toFixed(2), v => CONFIG.visual.breath = v, CONFIG.visual.breath);
bindSlider("sFade", "vFade", v => v.toFixed(1), v => { CONFIG.visual.fade = v; }, CONFIG.visual.fade);  // base value; renderFrame scales it with camera distance
let densTimer = null;
bindSlider("sDens", "vDens", v => v.toFixed(2), v => {
  CONFIG.visual.density = v;
  clearTimeout(densTimer); densTimer = setTimeout(buildLattice, 350);
}, CONFIG.visual.density);
$("sNest").addEventListener("change", () => {
  CONFIG.visual.deepNest = $("sNest").checked;
  setTimeout(buildLattice, 50);
});
$("sBg").addEventListener("change", () => { CONFIG.visual.bg = $("sBg").value; applyBg(CONFIG.visual.view === "sheet" ? "dark" : CONFIG.visual.bg); });
bindSlider("sTime", "vTime", v => v.toFixed(2), v => CONFIG.camera.timeScale = v, CONFIG.camera.timeScale);
bindSlider("sFly", "vFly", v => v.toFixed(1), v => CONFIG.camera.flySpeed = v, CONFIG.camera.flySpeed);
bindSlider("sBloom", "vBloom", v => v.toFixed(2), v => {
  CONFIG.camera.bloom = v;
  bloomPass.strength = CONFIG.visual.bg === "dark" ? Math.max(v, 0.2) : v;
}, 0.12);
bindSlider("sPlanet", "vPlanet", v => v.toFixed(2) + "×", v => { CONFIG.camera.planetDetail = v; applyPlanetDetail(); }, CONFIG.camera.planetDetail);
$("sQual").addEventListener("change", () => {
  CONFIG.camera.quality = parseFloat($("sQual").value);
  renderer.setPixelRatio(Math.min(3.5, CONFIG.camera.quality * (window.devicePixelRatio || 1)));
  if (composer.setPixelRatio) composer.setPixelRatio(renderer.getPixelRatio());
  else composer.setSize(window.innerWidth, window.innerHeight);
});
$("selStr").addEventListener("input", () => {
  if (selected && majorBodies.includes(selected)) {
    selected.strength = parseFloat($("selStr").value);
    $("selStrVal").textContent = selected.strength.toFixed(2) + "×";
  }
});
$("bAddSun").addEventListener("click", () => enterPlacement("sys"));
$("bAddSunStar").addEventListener("click", () => enterPlacement("sun"));
$("bAddHeavy").addEventListener("click", () => enterPlacement("star"));
$("bAddBH").addEventListener("click", () => enterPlacement("bh"));
$("bAddNS").addEventListener("click", () => enterPlacement("ns"));
$("bAddPulsar").addEventListener("click", () => enterPlacement("pulsar"));
$("bAddMeteors").addEventListener("click", () => enterPlacement("meteors"));
$("bAddLight").addEventListener("click", () => enterPlacement("light"));
$("bClear").addEventListener("click", () => {
  for (const b of [...majorBodies]) removeBody(b);
  for (const m of [...meteors]) removeMeteor(m);
  for (const b of [...beams]) removeBeam(b);
  select(null);
});
document.querySelectorAll("#camSeg .segbtn").forEach(btn => btn.addEventListener("click", () => setCamMode(btn.dataset.cam)));
function setCamMode(m) {
  cam.mode = m;
  document.querySelectorAll("#camSeg .segbtn").forEach(b => b.classList.toggle("on", b.dataset.cam === m));
  $("hint").textContent = m === "cinematic"
    ? "◈ Cinematic drift — wheel: zoom · drag: nudge · P: pause · Space: free flight"
    : "✦ Free flight — WASD move · drag: look · right-drag: pan · wheel: fly · Q/E roll · Shift boost · Space: cinematic";
}
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  composer.setSize(window.innerWidth, window.innerHeight);
});

function refreshList() {
  const box = $("objList");
  if (!majorBodies.length && !meteors.length && !beams.length) {
    box.innerHTML = "<div style='color:#7f93b6;font-size:11px'>No masses yet — pure parallel lattice.</div>";
  } else {
    box.innerHTML = "";
    const addRow = (b, label) => {
      const pp = b.anchor ? b.anchor : (b.group ? b.group.position : null);
      const row = document.createElement("div");
      row.className = "objrow" + (selected === b ? " sel" : "");
      row.innerHTML = "<span class='nm'>" + label + " <small>" +
        (pp ? pp.toArray().map(v => v.toFixed(1)).join(", ") : "") + "</small></span>" +
        "<button class='rm' title='remove'>✕</button>";
      row.querySelector(".rm").addEventListener("click", (e) => {
        e.stopPropagation();
        if (meteors.includes(b)) removeMeteor(b);
        else if (beams.includes(b)) removeBeam(b);
        else if (majorBodies.includes(b)) removeBody(b);   // guard stale rows (already eaten/removed)
      });
      row.addEventListener("click", () => select(b));
      box.appendChild(row);
    };
    majorBodies.forEach(b => addRow(b, icon(b) + " " + b.name));
    meteors.forEach(m => addRow(m, "☄ meteor"));
    beams.forEach(b => addRow(b, "✦ light beam"));
  }
  $("bAddSun").disabled = majorBodies.length >= CONFIG.bodies.maxMajor;
  $("bAddSunStar").disabled = majorBodies.length >= CONFIG.bodies.maxMajor;
  $("bAddHeavy").disabled = majorBodies.length >= CONFIG.bodies.maxMajor;
  $("bAddBH").disabled = majorBodies.length >= CONFIG.bodies.maxMajor;
  $("bAddNS").disabled = majorBodies.length >= CONFIG.bodies.maxMajor;
  $("bAddPulsar").disabled = majorBodies.length >= CONFIG.bodies.maxMajor;
  $("bBHBinary").disabled = majorBodies.length + 2 > CONFIG.bodies.maxMajor;
  $("bNSBinary").disabled = majorBodies.length + 2 > CONFIG.bodies.maxMajor;
  $("bAddMeteors").disabled = meteors.length >= CONFIG.bodies.maxMeteors;
  $("bAddLight").disabled = beams.length >= CONFIG.bodies.maxBeams;
}
function icon(b) { return b.type === "star" ? "★" : b.type === "sun" ? "☀" : b.type === "bh" ? "◉" : b.type === "pulsar" ? "⚡" : "✳"; }

function removeBody(b) {
  if (!b || !b.anchor || !b.group) return;   // defensive: body already gone
  ghosts.push({ pos: b.anchor.clone(), gm: b.warpGM * b.strength });
  scene.remove(b.group);
  const i = majorBodies.indexOf(b); if (i >= 0) majorBodies.splice(i, 1);
  const pi = pickables.indexOf(b.core || (b.sys ? b.sys.sunMesh : null) || b.group.children[0]);
  if (b.sys) {
    for (const p of b.sys.planets) {
      scene.remove(p.trail.line);
      const j = planets.indexOf(p); if (j >= 0) planets.splice(j, 1);
      const k = pickables.indexOf(p.mesh); if (k >= 0) pickables.splice(k, 1);
      scene.remove(p.mesh);
    }
  }
  if (selected === b) select(null);
  refreshList(); syncMassUniforms();
}
function removeMeteor(m) {
  scene.remove(m.mesh); scene.remove(m.trail.line);
  const i = meteors.indexOf(m); if (i >= 0) meteors.splice(i, 1);
  const k = pickables.indexOf(m.mesh); if (k >= 0) pickables.splice(k, 1);
}
function removeBeam(b) {
  scene.remove(b.line); scene.remove(b.pts);
  const i = beams.indexOf(b); if (i >= 0) beams.splice(i, 1);
}

/* ------------------------------------------------------------------ */
/* 10b. Physical phenomena — BH mergers, tidal capture, debris          */
/* ------------------------------------------------------------------ */
const BH_MERGE_RANGE = 9.0, BH_MERGE_DIST = 1.3;
const CAPTURE_RANGE = 11.5, DISRUPT_RANGE = 10.5;   // tuned to the lattice node spacing + well extent
const ripples = [], debrisPts = [], disruptions = [], flashes = [], rays = [];

function velOf(b) { if (!b._vel) b._vel = new THREE.Vector3(); return b._vel; }

/* expanding shockwave ring at a merger */
function spawnRipple(pos, size) {
  const mat = new THREE.MeshBasicMaterial({ color: 0xfff3d0, transparent: true, opacity: 0.85, depthWrite: false, side: THREE.DoubleSide });
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.35, 0.055, 8, 72), mat);
  ring.rotation.x = Math.PI / 2;                     // lie flat on the fabric plane
  ring.position.copy(pos);
  scene.add(ring);
  ripples.push({ mesh: ring, t: 0, max: 1.8, size });
}
/* glowing merger debris */
function spawnDebris(pos, n) {
  for (let i = 0; i < n && debrisPts.length < 120; i++) {
    const mesh = new THREE.Mesh(new THREE.SphereGeometry(0.045, 6, 4),
      new THREE.MeshBasicMaterial({ color: 0xffd9a0, transparent: true, opacity: 0.95 }));
    mesh.position.copy(pos).add(new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).multiplyScalar(0.8));
    scene.add(mesh);
    debrisPts.push({ mesh, vel: new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).multiplyScalar(1.3), life: 2.2 + Math.random() * 1.6 });
  }
}
/* radiation burst — a bright flash plus glowing rays fired outward when the
   black hole consumes something (star, planet, neutron star, meteor, …) */
function radiationBurst(pos, strength) {
  spawnDebris(pos, Math.round(18 * strength));
  const flash = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowWhite, color: 0xfff3d0, transparent: true, opacity: 0.95, depthWrite: false, blending: THREE.AdditiveBlending }));
  flash.position.copy(pos);
  scene.add(flash);
  flashes.push({ mesh: flash, t: 0, max: 0.9, size: 2.6 * strength + 1 });
  const n = Math.round(9 * strength);
  for (let i = 0; i < n; i++) {
    const dir = new THREE.Vector3(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize();
    const cone = new THREE.Mesh(new THREE.ConeGeometry(0.06, 1, 6, 1, true),
      new THREE.MeshBasicMaterial({ color: 0xffe9b0, transparent: true, opacity: 0.85, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide }));
    cone.position.copy(pos).addScaledVector(dir, 0.5);
    cone.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);
    scene.add(cone);
    rays.push({ mesh: cone, dir, t: 0, max: 0.9 + Math.random() * 0.5, len: 2 + Math.random() * 2.2 });
  }
}
function updateFx(dt) {
  for (let i = ripples.length - 1; i >= 0; i--) {
    const r = ripples[i];
    r.t += dt;
    const f = Math.min(1, r.t / r.max);
    r.mesh.scale.setScalar(1 + f * r.size);
    r.mesh.material.opacity = 0.85 * (1 - f);
    if (f >= 1) { scene.remove(r.mesh); r.mesh.geometry.dispose(); r.mesh.material.dispose(); ripples.splice(i, 1); }
  }
  for (let i = debrisPts.length - 1; i >= 0; i--) {
    const d = debrisPts[i];
    d.life -= dt;
    d.mesh.position.addScaledVector(d.vel, dt);
    d.vel.multiplyScalar(Math.exp(-dt * 0.6));
    d.mesh.material.opacity = Math.max(0, Math.min(1, d.life / 1.2));
    if (d.life <= 0) { scene.remove(d.mesh); d.mesh.geometry.dispose(); d.mesh.material.dispose(); debrisPts.splice(i, 1); }
  }
  /* radiation flashes expand and fade */
  for (let i = flashes.length - 1; i >= 0; i--) {
    const f = flashes[i];
    f.t += dt;
    const k = Math.min(1, f.t / f.max);
    f.mesh.scale.setScalar(1 + k * f.size);
    f.mesh.material.opacity = 0.95 * (1 - k);
    if (k >= 1) { scene.remove(f.mesh); f.mesh.material.dispose(); flashes.splice(i, 1); }
  }
  /* radiation rays shoot outward and fade */
  for (let i = rays.length - 1; i >= 0; i--) {
    const r = rays[i];
    r.t += dt;
    const k = Math.min(1, r.t / r.max);
    r.mesh.scale.set(1 + k * r.len * 0.4, 1 + k * r.len, 1 + k * r.len * 0.4);
    r.mesh.material.opacity = 0.85 * (1 - k);
    r.mesh.position.addScaledVector(r.dir, dt * r.len * 0.5);
    if (k >= 1) { scene.remove(r.mesh); r.mesh.geometry.dispose(); r.mesh.material.dispose(); rays.splice(i, 1); }
  }
}

/* ---- Black hole + black hole: mutual gravity → inspiral → merger ---- */
function mergeBHs(a, c) {
  if (a.merging || c.merging) return;
  a.merging = c.merging = true;
  const pos = a.anchor.clone().lerp(c.anchor, 0.5);
  spawnRipple(pos, 7);
  spawnDebris(pos, 42);
  radiationBurst(pos, 1.5);
  ghosts.push({ pos: pos.clone(), gm: (a.warpGM + c.warpGM) * 1.5, decay: 1 });   // fabric surge
  const gmSum = a.GM + c.GM, stSum = Math.min(3, (a.strength + c.strength) * 0.75);
  removeBody(a); removeBody(c);
  addBlackHole(pos);
  const nb = majorBodies[majorBodies.length - 1];
  if (nb) {
    nb.name = "Merged Black Hole";
    nb.GM = Math.min(6, gmSum);
    nb.warpGM = Math.min(4, Math.max(a.warpGM, c.warpGM) * 1.35);   // deeper well, wider W-opening
    nb.strength = stSum;
    nb.group.scale.setScalar(1.4);    // bigger event horizon, disk and jets
    select(nb);
    refreshList();
  }
}

/* ---- Tidal capture: BH eats stars · NS tears stars apart ---- */
function beginDisruption(star, strong) {
  if (disruptions.length >= 3) return;
  star.disrupting = true;
  const dir = new THREE.Vector3().subVectors(strong.anchor, star.anchor);
  const d0 = Math.max(dir.length(), 0.6);
  const tang = new THREE.Vector3(-dir.z, 0, dir.x).normalize();
  velOf(star).addScaledVector(tang, 0.5 * Math.sqrt(strong.GM / d0));  // start spiralling inward
  const N = 200;
  const geo = new THREE.BufferGeometry();
  const posA = new Float32Array(N * 3), colA = new Float32Array(N * 3);
  geo.setAttribute("position", new THREE.BufferAttribute(posA, 3));
  geo.setAttribute("color", new THREE.BufferAttribute(colA, 3));
  const pts = new THREE.Points(geo, new THREE.PointsMaterial({
    size: 0.1, map: glowWhite, vertexColors: true, transparent: true,
    depthWrite: false, blending: THREE.AdditiveBlending }));
  pts.visible = false;
  scene.add(pts);
  const parts = [];
  for (let i = 0; i < N; i++) parts.push({ r: 0.4 + Math.random() * 2.6, a: Math.random() * Math.PI * 2, y: (Math.random() - 0.5) * 0.3, active: 0 });
  disruptions.push({ star, strong, t: 0, max: 8, minT: 2.8, parts, pts, done: false, fade: 1 });
}
function coreOf(b) { return b.core || (b.sys ? b.sys.sunMesh : null); }
function cleanupDisruption(dis) {
  scene.remove(dis.pts);
  dis.pts.geometry.dispose(); dis.pts.material.dispose();
  const cm = coreOf(dis.star);
  if (cm) { cm.scale.set(1, 1, 1); if (cm.material.color) cm.material.color.set(0xffffff); }
  if (dis.star) dis.star.disrupting = false;
}
function advanceDisruptions(dt) {
  for (let di = disruptions.length - 1; di >= 0; di--) {
    const dis = disruptions[di];
    const { star, strong } = dis;
    if (!majorBodies.includes(strong) || !majorBodies.includes(star)) {   // object removed mid-tear
      cleanupDisruption(dis); disruptions.splice(di, 1); continue;
    }
    dis.t += dt;
    if (!dis.done) {
      const d = star.anchor.distanceTo(strong.anchor);
      const swallow = strong.type === "bh" ? BH_R * 1.15 : 0.22;
      /* pull the star inward + tangential drift → graceful spiral into the strong body */
      const dir = new THREE.Vector3().subVectors(strong.anchor, star.anchor);
      const len = Math.max(dir.length(), 0.01);
      const v = velOf(star);
      v.addScaledVector(dir, dt * 0.9 / len);     // gentler pull → long cinematic spiral
      v.multiplyScalar(Math.exp(-dt * 0.22));
      star.anchor.addScaledVector(v, dt);
      /* the captured object stretches along the radial direction and reddens as it approaches */
      const f = Math.min(1, dis.t / (dis.max * 0.75));
      const cm = coreOf(star);
      if (cm) {
        cm.scale.set(1 + 2.0 * f, Math.max(0.15, 1 - 0.6 * f), Math.max(0.15, 1 - 0.6 * f));
        if (cm.material.color) cm.material.color.setRGB(Math.min(1, 1.6 * (1 - f)), 0.95 * (1 - f), 0.85 * (1 - f));
      }
      /* glowing stream of torn material spirals into the strong body */
      const posA = dis.pts.geometry.attributes.position.array;
      const colA = dis.pts.geometry.attributes.color.array;
      for (let i = 0; i < dis.parts.length; i++) {
        const p = dis.parts[i];
        if (p.active === 0) {
          if (Math.random() < 0.12) {
            p.active = 1;
            p.r = Math.max(0.4, d * 0.85);
            p.a = Math.atan2(star.anchor.z - strong.anchor.z, star.anchor.x - strong.anchor.x);
            p.y = (Math.random() - 0.5) * 0.3;
          } else { posA[i * 3] = 1e6; posA[i * 3 + 1] = 1e6; posA[i * 3 + 2] = 1e6; continue; }
        }
        p.r = Math.max(0.06, p.r * (1 - dt * 0.5));
        p.a += dt * (2.2 / Math.max(p.r, 0.12));
        p.y *= (1 - dt * 0.6);
        const px = strong.anchor.x + p.r * Math.cos(p.a);
        const pz = strong.anchor.z + p.r * Math.sin(p.a);
        posA[i * 3] = px;
        posA[i * 3 + 1] = strong.anchor.y + p.y - (CONFIG.visual.view === "sheet" ? wellAt(px, pz) : 0);
        posA[i * 3 + 2] = pz;
        const hot = p.r < 0.7 ? 1 : 0.4 / p.r;   // white-hot near the strong body
        colA[i * 3] = 1; colA[i * 3 + 1] = 0.75 * hot + 0.2; colA[i * 3 + 2] = 0.45 * hot;
      }
      dis.pts.geometry.attributes.position.needsUpdate = true;
      dis.pts.geometry.attributes.color.needsUpdate = true;
      dis.pts.visible = true;
      /* never an instant swallow — the tear is always visible for at least minT */
      if ((d < swallow && dis.t > dis.minT) || dis.t > dis.max) {
        dis.done = true;
        ghosts.push({ pos: strong.anchor.clone(), gm: Math.max(0.4, star.warpGM * 1.2), decay: 1 });
        radiationBurst(strong.anchor, strong.type === "bh" ? 1 : 0.7);   // radiation flash as it is consumed
        removeBody(star);
      }
    } else {
      dis.fade -= dt * 0.5;
      dis.pts.material.opacity = Math.max(0, dis.fade);
      if (dis.fade <= 0) { cleanupDisruption(dis); disruptions.splice(di, 1); }
    }
  }
}

function updateInteractions(dt) {
  advanceDisruptions(dt);
  /* black-hole pairs: mutual gravity, inspiral, then merger */
  const bhs = majorBodies.filter(b => b.type === "bh");
  for (let i = 0; i < bhs.length; i++) {
    for (let j = i + 1; j < bhs.length; j++) {
      const a = bhs[i], c = bhs[j];
      if (a.merging || c.merging) continue;
      const dir = new THREE.Vector3().subVectors(c.anchor, a.anchor);
      const d = dir.length();
      if (d < BH_MERGE_DIST) { mergeBHs(a, c); break; }
      if (d < BH_MERGE_RANGE) {
        const avgG = (a.GM + c.GM) * 0.5;
        const nd = dir.clone().divideScalar(Math.max(d, 0.1));
        const acc = 0.8 * avgG / (d * d);
        if (!a._tangent) {   // seed tangential motion once → graceful inspiral
          const tang = new THREE.Vector3(-nd.z, 0, nd.x);
          const spd = 0.5 * Math.sqrt(avgG / d);
          velOf(a).addScaledVector(tang, spd);
          velOf(c).addScaledVector(tang, -spd);
          a._tangent = c._tangent = true;
        }
        velOf(a).addScaledVector(nd, acc * dt);
        velOf(c).addScaledVector(nd, -acc * dt);
      }
    }
  }
  /* capture: a black hole eats ANYTHING near it — stars, planets, neutron
     stars, pulsars, whole solar systems. A neutron star tears stars apart.
     Only a BH next to another BH is excluded — that follows the merger path. */
  for (const b of majorBodies) {
    if (b.type !== "bh" && b.type !== "ns") continue;
    const range = b.type === "bh" ? CAPTURE_RANGE : DISRUPT_RANGE;
    for (const s of majorBodies) {
      if (s === b || s.disrupting) continue;
      if (b.type === "bh" && s.type === "bh") continue;
      if (b.type === "ns" && (s.type === "ns" || s.type === "pulsar")) continue;
      if (b.anchor.distanceTo(s.anchor) < range) {
        beginDisruption(s, b);
        break;
      }
    }
  }
  /* advance every body that is dynamically moving (mild drag → graceful spirals) */
  for (const b of majorBodies) {
    if (!b._vel) continue;
    b._vel.multiplyScalar(Math.exp(-dt * 0.12));
    if (b._vel.lengthSq() < 1e-8) continue;
    b.anchor.addScaledVector(b._vel, dt);
  }
}

/* ------------------------------------------------------------------ */
/* 11. Main loop                                                       */
/* ------------------------------------------------------------------ */
const clock = new THREE.Clock();
let time = 0, paused = false, fpsEma = 60, lastRo = 0;
const readEl = $("readout");

function readDelta(b) {
  const w = b.warpGM * b.strength * (b.pulse ? 1.35 : 1) * CONFIG.visual.warpMul;
  return deltaEff(w, 1.0) * 100;
}
/* show tiny weak-field Δ in scientific notation so the exact magnitude is visible */
function fmtDelta(dlt) {
  return dlt >= 0.005 ? dlt.toFixed(2) + "%" : "≈0 (" + dlt.toExponential(1) + "%)";
}

function updateBodies(dt) {
  updateInteractions(dt);
  refreshDynBodies();
  updateFx(dt);
  for (const b of majorBodies) {
    if (b.type === "sun") { if (b.sys) b.sys.sunMesh.rotation.y += dt * 0.15; else if (b.core) b.core.rotation.y += dt * 0.15; }
    if (b.type === "star") { if (b.core) b.core.rotation.y += dt * 0.12; }
    if (b.type === "ns") {
      b.spinAngle += dt * 3.2;
      b.group.rotation.y = b.spinAngle * 0.7;
      const p = 0.75 + 0.25 * Math.sin(b.spinAngle * 3);
      b.core.material.color.setRGB(0.87 * p, 0.94 * p, 1.0 * p);
    }
    if (b.type === "pulsar") {
      b.spinAngle += dt * 4.5;
      b.group.rotation.y = b.spinAngle;
      const p = 0.7 + 0.3 * Math.sin(b.spinAngle * 2);
      b.core.material.color.setRGB(0.95 * p, 0.98 * p, 1.0);
      if (b.beamMat) b.beamMat.opacity = 0.3 + 0.3 * Math.sin(b.spinAngle * 2);
    }
    if (b.type === "bh") {
      b.spinAngle += dt;
      for (let i = 0; i < b.diskData.length; i++) {
        const d = b.diskData[i], om = Math.sqrt(BH_GM / Math.pow(d.r, 3));
        const a = d.a + b.spinAngle * om;
        const y = d.th * (1 + 0.4 * Math.sin(a * 3 + d.r * 5));
        b.disk.geometry.attributes.position.array[i * 3] = Math.cos(a) * d.r;
        b.disk.geometry.attributes.position.array[i * 3 + 1] = y;
        b.disk.geometry.attributes.position.array[i * 3 + 2] = Math.sin(a) * d.r;
      }
      b.disk.geometry.attributes.position.needsUpdate = true;
      for (let i = 0; i < b.jData.length; i++) {
        const j = b.jData[i];
        j.t += dt * 0.35;
        if (j.t > 1) { j.t = 0; j.side = Math.random() < 0.5 ? 1 : -1; j.off = (Math.random() - 0.5) * 0.12; }
        const y = (0.9 + j.t * 4.2) * j.side;
        b.jPos[i * 3] = j.off * Math.sin(b.spinAngle * 2 + i); b.jPos[i * 3 + 1] = y; b.jPos[i * 3 + 2] = j.off * Math.cos(b.spinAngle * 2 + i);
      }
      b.jPos.needsUpdate = true;
    }
  }
  /* planets */
  const sub = 3, sdt = dt / sub;
  for (const p of planets) {
    p.hist.unshift(p.worldPos.clone()); if (p.hist.length > p.trail.n) p.hist.length = p.trail.n;
    for (let s = 0; s < sub; s++) stepBody(p.worldPos, p.vel, sdt);
    p.mesh.position.copy(p.worldPos).sub(p.system.group.position);
    p.mesh.rotation.y += dt * p.spinSpeed;              // slow self-rotation
    updateTrail(p.trail, p.hist);
  }
  /* meteors */
  for (let mi = meteors.length - 1; mi >= 0; mi--) {
    const m = meteors[mi];
    m.hist.unshift(m.worldPos.clone()); if (m.hist.length > m.trail.n) m.hist.length = m.trail.n;
    for (let s = 0; s < sub; s++) stepBody(m.worldPos, m.vel, sdt);
    if (CONFIG.visual.view === "sheet") m.mesh.position.set(m.worldPos.x, m.worldPos.y - wellAt(m.worldPos.x, m.worldPos.z), m.worldPos.z);
    else m.mesh.position.copy(m.worldPos);
    m.mesh.rotateOnAxis(m.rotAxis, m.rotSpeed * dt);
    updateTrail(m.trail, m.hist);
    for (const b of majorBodies) {
      const d = m.worldPos.distanceTo(b.anchor);
      if ((b.type === "bh" && d < BH_R * 0.9) || (b.type === "ns" && d < 0.22) || (b.type === "pulsar" && d < 0.24)) {
        if (b.type === "bh") radiationBurst(b.anchor, 0.3);   // small radiation pop as the BH eats a meteor
        removeMeteor(m); break;
      }
    }
  }
  /* beams */
  for (const b of beams) {
    b.life -= dt; b.t += dt * 0.8;
    if (b.life <= 0) { removeBeam(b); continue; }
    const steps = 220, sdt2 = 0.05;
    const p = b.pos.clone(), v = b.dir.clone().multiplyScalar(C_LIGHT);
    const arr = new Float32Array(steps * 3);
    for (let s = 0; s < steps; s++) {
      stepPhoton(p, v, sdt2);
      arr[s * 3] = p.x;
      arr[s * 3 + 1] = p.y - (CONFIG.visual.view === "sheet" ? wellAt(p.x, p.z) : 0);
      arr[s * 3 + 2] = p.z;
    }
    /* light is captured by the event horizon — truncate the beam where it crosses */
    let cut = steps;
    for (let s = 0; s < steps; s++) {
      const hx = arr[s * 3], hz = arr[s * 3 + 2];
      let eaten = false;
      for (const hb of majorBodies) {
        if (hb.type === "bh" && Math.hypot(hx - hb.anchor.x, hz - hb.anchor.z) < BH_R) { eaten = true; break; }
      }
      if (eaten) { cut = s; break; }
    }
    const arr2 = cut < steps ? arr.slice(0, cut * 3) : arr;
    b.line.geometry.setAttribute("position", new THREE.BufferAttribute(arr2, 3));
    b.line.geometry.attributes.position.needsUpdate = true;
    b.line.material.opacity = 0.55 * Math.min(1, b.life / 2);
    const pn = 36, pArr = new Float32Array(pn * 3);
    const span = Math.max(cut, 1);
    for (let i = 0; i < pn; i++) {
      const idx = Math.floor((b.t * 9 + i * 2.2) % span);
      pArr[i * 3] = arr[idx * 3]; pArr[i * 3 + 1] = arr[idx * 3 + 1]; pArr[i * 3 + 2] = arr[idx * 3 + 2];
    }
    b.pts.geometry.setAttribute("position", new THREE.BufferAttribute(pArr, 3));
    b.pts.geometry.attributes.position.needsUpdate = true;
  }
  /* ambient photons */
  for (const p of aPhot) {
    if (!p) continue;
    p.life -= dt;
    if (p.life <= 0) { spawnAmbient(null, false); continue; }
    for (let s = 0; s < sub; s++) stepPhoton(p.pos, p.vel, sdt);
    for (const b of majorBodies) {
      const d = p.pos.distanceTo(b.anchor);
      if ((b.type === "bh" && d < BH_R) || (b.type === "ns" && d < 0.2)) { spawnAmbient(null, false); break; }
    }
  }
  for (let i = 0; i < AMBIENT_N; i++) {
    const p = aPhot[i];
    if (!p) { aPos[i * 3] = 1e6; aPos[i * 3 + 1] = 1e6; aPos[i * 3 + 2] = 1e6; continue; }
    aPos[i * 3] = p.pos.x;
    aPos[i * 3 + 1] = p.pos.y - (CONFIG.visual.view === "sheet" ? wellAt(p.pos.x, p.pos.z) : 0);
    aPos[i * 3 + 2] = p.pos.z;
  }
  aGeo.attributes.position.needsUpdate = true;
  /* ghosts decay */
  for (let i = ghosts.length - 1; i >= 0; i--) {
    ghosts[i].decay *= Math.exp(-dt * 2.2);
    if (ghosts[i].decay < 0.02) ghosts.splice(i, 1);
  }
  syncMassUniforms();
}

function renderFrame() {
  const dtRaw = Math.min(clock.getDelta(), 0.05);
  const dt = paused ? 0 : dtRaw * CONFIG.camera.timeScale;
  time += dt;
  fpsEma += (dtRaw > 0 ? 1 / dtRaw : 60) - fpsEma; fpsEma *= 0.98;

  updateCamera(dtRaw);
  updateBodies(dt);

  /* visual well sink — objects rest at the bottom of their own funnels */
  for (const b of majorBodies) {
    if (CONFIG.visual.view === "sheet") b.group.position.set(b.anchor.x, b.anchor.y - wellAt(b.anchor.x, b.anchor.z), b.anchor.z);
    else b.group.position.copy(b.anchor);
  }

  /* material uniforms */
  shared.uTime.value = time;
  /* zoom-independent clarity: scale the distance fade with camera distance so the
     fabric never washes out or blurs when you zoom out — it stays crisp at any zoom */
  const camDist = camera.position.distanceTo(latticeCenter);
  shared.uFadeNear.value = Math.max(CONFIG.visual.fade, camDist * 1.5 + 6);
  shared.uFadeFar.value = shared.uFadeNear.value + Math.max(10, camDist * 0.5);
  shared.uN.value = CONFIG.metric.n;
  shared.uPhi0.value = CONFIG.metric.phi0;
  shared.uAlpha.value = CONFIG.metric.alpha;
  shared.uDistort.value = CONFIG.visual.distort;
  shared.uWScale.value = CONFIG.visual.wScale;
  shared.uBreath.value = 0.006 * Math.sin(time * 0.35) * CONFIG.visual.breath;
  sharedAll();
  for (const m of fabricMats) {
    const ph = (time * 0.12 * CONFIG.visual.wave + m.userData.phase) % 1;
    m.uniforms.uPulse.value = Math.pow(Math.sin(Math.PI * ph), 2);
  }
  sheetMats.forEach(m => { m.uniforms.uWellDepth.value = CONFIG.visual.wellDepth; m.uniforms.uGridR.value = GRID_SPAN * L; });

  /* selection ring */
  if (selected) {
    selRing.visible = true;
    selRing.position.copy(selected.group ? selected.group.position : selected.worldPos);
    selRing.scale.setScalar(selected.type === "bh" ? 1.3 : selected.type === "sun" ? 1.9 : selected.type === "ns" ? 0.8 : selected.type === "pulsar" ? 0.7 : 0.9);
    selRing.rotation.x += dt * 0.5; selRing.rotation.y += dt * 0.3;
  } else selRing.visible = false;

  if (reticle.visible) reticle.lookAt(camera.position);

  composer.render();

  /* readout (~3 Hz) */
  if (time - lastRo > 0.33) {
    lastRo = time;
    let strongest = null;
    for (const b of majorBodies) if (!strongest || b.warpGM * b.strength > strongest.warpGM * strongest.strength) strongest = b;
    const dlt = strongest ? readDelta(strongest) : 0;
    /* Δ and D(r) must come from the SAME local potential Φ = warpGM/r at r = 1,
       exactly as deltaEff() evaluates it — no separate fudge factor */
    const w = strongest ? strongest.warpGM * strongest.strength * (strongest.pulse ? 1.35 : 1) * CONFIG.visual.warpMul : 0;
    const x = Math.pow(Math.max(w / CONFIG.metric.phi0, 0), CONFIG.metric.n);
    const D = 1 + CONFIG.metric.alpha * x / (1 + x);
    readEl.innerHTML =
      "<b>FPS</b>        " + Math.round(fpsEma) + "\n" +
      "<b>" + (CONFIG.visual.view === "sheet" ? "Sheet grid" : CONFIG.visual.view === "5d" ? "5D lattice" : "Instances") + "</b>  " +
        (CONFIG.visual.view === "sheet"
          ? CONFIG._grid.verts.toLocaleString() + " pts · " + CONFIG._grid.segs.toLocaleString() + " lines"
          : (CONFIG._instances || 0).toLocaleString()) + "\n" +
      "<b>Mode</b>       " + (cam.mode === "cinematic" ? "Cinematic drift" : "Free flight") + (paused ? "  (paused)" : "") + "\n" +
      "<b>Δ (Lucky)</b>  " + (strongest ? strongest.name + ": " + fmtDelta(dlt) : "—") + "\n" +
      "<b>D(r)/ℓ²</b>    " + (strongest ? D.toFixed(4) : "1.0000") + (strongest && D > 1.01 ? "  ⇧ threshold open" : "") + "\n" +
      "<b>Masses</b>     " + majorBodies.length + "  ·  " + "beams " + beams.length + "  ·  photons " + AMBIENT_N + "\n" +
      "<b>Params</b>     n=" + CONFIG.metric.n.toFixed(1) + " Φ₀=" + CONFIG.metric.phi0.toFixed(3) + " α=" + CONFIG.metric.alpha.toFixed(3) + " ℓ=" + CONFIG.metric.ell.toFixed(1) + " km";
    $("fps").textContent = Math.round(fpsEma) + " fps";
  }
}
renderer.setAnimationLoop(renderFrame);

/* ------------------------------------------------------------------ */
/* 12. Hawking Radiation — post-accretion glow + evaporation mode       */
/* ------------------------------------------------------------------ */
/* Hawking temperature: T_H = ℏc³ / (8π G M k_B). In our natural units,
   T_H ∝ 1/M. A solar-mass BH has T_H ≈ 60 nK (invisible); a micro-BH
   (M ~ 10⁻⁵ M☉) would glow hot. We visualise the radiation as a soft
   expanding glow whose colour and intensity depend on T_H. */
const HAWKING_HBAR = 1.0546e-34, HAWKING_G = 6.674e-11, HAWKING_C = 3e8, HAWKING_KB = 1.381e-23;
const SOLAR_KG = 1.989e30;
const hawkingGlows = [];   // { mesh, bhRef, t, maxLife }
const evapEnabled = { value: false };

function hawkingTemp(M_solar) {
  /* T_H in Kelvin for a black hole of mass M_solar solar masses */
  const M = M_solar * SOLAR_KG;
  return (HAWKING_HBAR * Math.pow(HAWKING_C, 3)) / (8 * Math.PI * HAWKING_G * M * HAWKING_KB);
}
function hawkingWavelength(T) {
  /* peak wavelength via Wien's displacement law: λ_max = b/T, b ≈ 2.898e-3 m·K */
  return T > 0 ? 2.898e-3 / T : 1e10;
}
function hawkingPower(M_solar) {
  /* Stefan-Boltzmann-like luminosity: L = ℏc⁶ / (15360 π G² M²) */
  const M = M_solar * SOLAR_KG;
  return (HAWKING_HBAR * Math.pow(HAWKING_C, 6)) / (15360 * Math.PI * HAWKING_G * HAWKING_G * M * M);
}

function spawnHawkingGlow(bh) {
  /* soft expanding thermally-coloured sprite */
  const T = hawkingTemp(bh.GM * 0.001);   // scale to sim units → solar masses
  /* colour from temperature: hot = blue-white, cold = dim red */
  let r, g, b;
  if (T > 1e4) { r = 0.85; g = 0.9; b = 1.0; }       // hot: blue-white
  else if (T > 1e2) { r = 1.0; g = 0.95; b = 0.8; }   // warm: yellow-white
  else { r = 1.0; g = 0.55; b = 0.25; }                 // cold: deep orange-red
  const mat = new THREE.SpriteMaterial({
    map: glowWhite, color: new THREE.Color(r, g, b),
    transparent: true, opacity: 0.7, depthWrite: false,
    blending: THREE.AdditiveBlending
  });
  const sp = new THREE.Sprite(mat);
  sp.position.copy(bh.anchor);
  sp.scale.setScalar(0.5);
  scene.add(sp);
  hawkingGlows.push({ mesh: sp, bhRef: bh, t: 0, maxLife: 6, baseScale: 0.5 });
}

function updateHawking(dt) {
  /* spawn new glows periodically for each BH */
  for (const b of majorBodies) {
    if (b.type !== "bh") continue;
    b._hawkingTimer = (b._hawkingTimer || 0) + dt;
    if (b._hawkingTimer > 2.5) {
      b._hawkingTimer = 0;
      spawnHawkingGlow(b);
    }
  }
  /* update existing glows — expand, fade, consume */
  for (let i = hawkingGlows.length - 1; i >= 0; i--) {
    const h = hawkingGlows[i];
    h.t += dt;
    if (!majorBodies.includes(h.bhRef)) { scene.remove(h.mesh); h.mesh.material.dispose(); hawkingGlows.splice(i, 1); continue; }
    const f = Math.min(1, h.t / h.maxLife);
    h.mesh.position.copy(h.bhRef.anchor);
    h.mesh.scale.setScalar(h.baseScale + f * 5);
    h.mesh.material.opacity = 0.7 * (1 - f) * Math.min(1, h.bhRef.GM * 0.6);
    if (f >= 1) { scene.remove(h.mesh); h.mesh.material.dispose(); hawkingGlows.splice(i, 1); }
  }
  /* evaporation mode: BH slowly loses mass */
  if (evapEnabled.value) {
    for (const b of majorBodies) {
      if (b.type !== "bh") continue;
      const evapRate = 0.000015 / Math.max(b.GM * b.GM, 0.01);   // smaller BHs evaporate faster
      b.GM *= Math.exp(-dt * evapRate);
      b.warpGM *= Math.exp(-dt * evapRate);
      b.strength *= Math.exp(-dt * evapRate * 0.5);
      /* visual shrinking */
      if (b.core) {
        const s = Math.max(0.08, b.GM / BH_GM);
        b.core.scale.setScalar(s);
      }
      if (b.GM < 0.01) {
        /* BH fully evaporated — radiation burst + removal */
        radiationBurst(b.anchor, 1.2);
        removeBody(b);
      }
    }
  }
}

/* ------------------------------------------------------------------ */
/* 13. Binary Star Collision & Merger Physics                          */
/* ------------------------------------------------------------------ */
/* TOV limit ~2.17 M☉ — above this, a neutron star collapses to a BH */
const TOV_LIMIT = 2.17;
const binaries = [];   // { a, b, phase, phaseSpeed, mergerT, stage, meshes }

function initBinary(a, b) {
  const dist = a.anchor.distanceTo(b.anchor);
  const avgG = (a.GM + b.GM) * 0.5;
  const omega = Math.sqrt(avgG / Math.pow(Math.max(dist, 0.5), 3));
  binaries.push({
    a, b, phase: 0, phaseSpeed: omega * 0.8,
    mergerT: 0, maxMergerT: 12, stage: "inspiral",
    meshes: [], envelope: null, jets: [], kilonova: null
  });
}

function updateBinaries(dt) {
  for (let bi = binaries.length - 1; bi >= 0; bi--) {
    const bin = binaries[bi];
    if (!majorBodies.includes(bin.a) || !majorBodies.includes(bin.b)) {
      cleanupBinary(bin); binaries.splice(bi, 1); continue;
    }
    const d = bin.a.anchor.distanceTo(bin.b.anchor);
    bin.phase += bin.phaseSpeed * dt;
    bin.phaseSpeed *= 1 + dt * 0.12;   // GW-driven inspiral: orbital frequency increases
    /* tidal deformation — elongate both objects toward each other */
    const cmA = coreOf(bin.a), cmB = coreOf(bin.b);
    const dir = new THREE.Vector3().subVectors(bin.b.anchor, bin.a.anchor).normalize();
    const tidalF = Math.min(1.0, 3.0 / Math.max(d, 0.3));
    if (cmA) {
      const stretch = 1 + tidalF * 0.6;
      const compress = Math.max(0.3, 1 - tidalF * 0.35);
      cmA.scale.set(
        stretch * Math.abs(dir.x) + compress * (1 - Math.abs(dir.x)),
        stretch * Math.abs(dir.y) + compress * (1 - Math.abs(dir.y)),
        stretch * Math.abs(dir.z) + compress * (1 - Math.abs(dir.z))
      );
    }
    if (cmB) {
      const stretch = 1 + tidalF * 0.6;
      const compress = Math.max(0.3, 1 - tidalF * 0.35);
      cmB.scale.set(
        stretch * Math.abs(dir.x) + compress * (1 - Math.abs(dir.x)),
        stretch * Math.abs(dir.y) + compress * (1 - Math.abs(dir.y)),
        stretch * Math.abs(dir.z) + compress * (1 - Math.abs(dir.z))
      );
    }
    /* common envelope phase — shared glow when close */
    if (d < 3.5 && !bin.envelope) {
      const mid = bin.a.anchor.clone().lerp(bin.b.anchor, 0.5);
      const envMat = new THREE.SpriteMaterial({
        map: glowOran, color: 0xffd090, transparent: true, opacity: 0.55, depthWrite: false,
        blending: THREE.AdditiveBlending
      });
      bin.envelope = new THREE.Sprite(envMat);
      bin.envelope.position.copy(mid);
      bin.envelope.scale.setScalar(d * 1.8);
      scene.add(bin.envelope);
    }
    if (bin.envelope) {
      const mid = bin.a.anchor.clone().lerp(bin.b.anchor, 0.5);
      bin.envelope.position.copy(mid);
      bin.envelope.scale.setScalar(d * 1.8);
      bin.envelope.material.opacity = 0.3 + 0.35 * (1 - d / 3.5);
    }
    /* fabric-twisting animation — swirling distortion for NS binaries */
    const isNSBinary = (bin.a.type === "ns" || bin.a.type === "pulsar") && (bin.b.type === "ns" || bin.b.type === "pulsar");
    if (isNSBinary) {
      /* spin-up phase: create extra spin angles on both NS */
      bin.a.spinAngle += dt * bin.phaseSpeed * 2;
      bin.b.spinAngle += dt * bin.phaseSpeed * 2;
      /* asymmetric fabric twist — the fabric between them swirls */
      const twistStrength = Math.min(1.0, 5.0 / Math.max(d, 0.5));
      if (bin.a.group) bin.a.group.rotation.y += dt * bin.phaseSpeed * twistStrength;
      if (bin.b.group) bin.b.group.rotation.y += dt * bin.phaseSpeed * twistStrength;
    }
    /* GW-driven orbital decay: distance shrinks — avgG is the pair's
       combined GM (was referenced below without ever being defined here,
       which threw on the first frame of every binary, NS preset included) */
    const avgG = (bin.a.GM + bin.b.GM) * 0.5;
    const decayRate = 0.15 * avgG / (d * d);
    const moveDir = dir.clone().negate();
    bin.a.anchor.addScaledVector(moveDir, decayRate * dt * 0.5);
    bin.b.anchor.addScaledVector(dir, decayRate * dt * 0.5);
    /* merger threshold */
    if (d < 0.6) {
      bin.stage = "merger";
      bin.mergerT += dt;
      if (bin.mergerT > 0.3) {
        /* final merger */
        const totalGM = bin.a.GM + bin.b.GM;
        const totalWarp = Math.max(bin.a.warpGM, bin.b.warpGM) * 1.3;
        const pos = bin.a.anchor.clone().lerp(bin.b.anchor, 0.5);
        const bothCompact = (bin.a.type === "ns" || bin.a.type === "pulsar" || bin.a.type === "bh") &&
                           (bin.b.type === "ns" || bin.b.type === "pulsar" || bin.b.type === "bh");
        /* kilonova glow */
        const knMat = new THREE.SpriteMaterial({
          map: glowOran, color: 0xffeebb, transparent: true, opacity: 0.9, depthWrite: false,
          blending: THREE.AdditiveBlending
        });
        bin.kilonova = new THREE.Sprite(knMat);
        bin.kilonova.position.copy(pos);
        bin.kilonova.scale.setScalar(1);
        scene.add(bin.kilonova);
        /* relativistic jets */
        for (const sign of [-1, 1]) {
          const jetGeo = new THREE.CylinderGeometry(0.02, 0.16, 5, 10, 1, true);
          const jetMat = new THREE.MeshBasicMaterial({ color: 0xbfe0ff, transparent: true, opacity: 0.6, depthWrite: false });
          const jet = new THREE.Mesh(jetGeo, jetMat);
          jet.position.copy(pos);
          jet.position.y += sign * 2.5;
          scene.add(jet);
          bin.jets.push(jet);
        }
        /* strong fabric ripple */
        spawnRipple(pos, 9);
        spawnDebris(pos, 50);
        radiationBurst(pos, 1.8);
        ghosts.push({ pos: pos.clone(), gm: totalWarp * 1.4, decay: 1 });
        /* remove the two original objects */
        removeBody(bin.a); removeBody(bin.b);
        cleanupBinary(bin);
        /* decide outcome based on total mass */
        if (bothCompact && totalGM > TOV_LIMIT) {
          /* above TOV → collapse to black hole */
          addBlackHole(pos);
          const nb = majorBodies[majorBodies.length - 1];
          if (nb) {
            nb.name = "Merger Remnant (BH)";
            nb.GM = Math.min(7, totalGM);
            nb.warpGM = Math.min(5, totalWarp);
            nb.group.scale.setScalar(1.3);
            select(nb);
          }
        } else if (bothCompact) {
          /* below TOV → hypermassive NS (temporarily brighter) */
          addNeutronStar(pos);
          const nb = majorBodies[majorBodies.length - 1];
          if (nb) {
            nb.name = "Remnant (hypermassive NS)";
            nb.GM = totalGM;
            nb.warpGM = totalWarp;
            nb.pulse = true;
            nb.spinAngle = 0;
            select(nb);
          }
        } else {
          /* two ordinary stars → merged heavier star */
          addHeavyStar(pos);
          const nb = majorBodies[majorBodies.length - 1];
          if (nb) {
            nb.name = "Merged Star";
            nb.GM = totalGM;
            nb.warpGM = totalWarp;
            select(nb);
          }
        }
        binaries.splice(bi, 1);
        refreshList(); syncMassUniforms();
        return;
      }
    }
    /* update positions of orbiting visuals */
    const sep = d * 0.5;
    const ax = new THREE.Vector3().crossVectors(dir, new THREE.Vector3(0, 1, 0)).normalize();
    if (ax.lengthSq() < 0.01) ax.set(1, 0, 0);
    bin.a.anchor.addScaledVector(ax, Math.sin(bin.phase) * sep * 0.02);
    bin.b.anchor.addScaledVector(ax, -Math.sin(bin.phase) * sep * 0.02);
    /* common envelope pulse */
    if (bin.envelope) bin.envelope.material.opacity *= 0.995 + 0.005 * Math.sin(bin.phase * 3);
    /* kilonova expanding glow during merger */
    if (bin.kilonova) {
      bin.kilonova.scale.setScalar(1 + bin.mergerT * 3);
      bin.kilonova.material.opacity = Math.max(0, 0.9 - bin.mergerT * 0.3);
    }
  }
}

function cleanupBinary(bin) {
  if (bin.envelope) { scene.remove(bin.envelope); bin.envelope.material.dispose(); }
  for (const j of bin.jets) { scene.remove(j); j.geometry.dispose(); j.material.dispose(); }
  if (bin.kilonova) { scene.remove(bin.kilonova); bin.kilonova.material.dispose(); }
}

/* ------------------------------------------------------------------ */
/* 14. NS Binary Preset                                               */
/* ------------------------------------------------------------------ */
function placeNSBinary(pos) {
  if (majorBodies.length + 2 > CONFIG.bodies.maxMajor) return;
  const sep = 2.8;   // close separation for tight orbit
  const p1 = pos.clone().add(new THREE.Vector3(-sep / 2, 0, 0));
  const p2 = pos.clone().add(new THREE.Vector3(sep / 2, 0, 0));
  const ns1 = addNeutronStar(p1);
  const ns2 = addNeutronStar(p2);
  if (ns1 && ns2) {
    ns1.name = "NS Binary A";
    ns2.name = "NS Binary B";
    /* seed tangential velocities for circular orbit */
    const avgG = (ns1.GM + ns2.GM) * 0.5;
    const orbV = Math.sqrt(avgG / sep) * 0.7;
    velOf(ns1).set(0, 0, orbV);
    velOf(ns2).set(0, 0, -orbV);
    initBinary(ns1, ns2);
    refreshList();
  }
}

/* ------------------------------------------------------------------ */
/* 14b. Black-Hole Binary Preset                                      */
/* ------------------------------------------------------------------ */
/* Mirrors placeNSBinary() above — two black holes on a collision
   course, driven end-to-end by the SAME engine in section 13:
   initBinary() binds the pair, updateBinaries() inspirals, tidally
   stretches and merges it, and the totalGM-vs-TOV_LIMIT check resolves
   it as "Merger Remnant (BH)" (2 × BH_GM = 3.6 > 2.17, always). */
function placeBHBinary(pos) {
  if (majorBodies.length + 2 > CONFIG.bodies.maxMajor) return;
  const sep = 3.2;   // slightly wider starting separation — reads well for BHs
  const p1 = pos.clone().add(new THREE.Vector3(-sep / 2, 0, 0));
  const p2 = pos.clone().add(new THREE.Vector3(sep / 2, 0, 0));
  const bh1 = addBlackHole(p1);
  const bh2 = addBlackHole(p2);
  if (bh1 && bh2) {
    bh1.name = "Black Hole A";
    bh2.name = "Black Hole B";
    /* seed tangential velocities for circular orbit */
    const avgG = (bh1.GM + bh2.GM) * 0.5;
    const orbV = Math.sqrt(avgG / sep) * 0.7;
    velOf(bh1).set(0, 0, orbV);
    velOf(bh2).set(0, 0, -orbV);
    initBinary(bh1, bh2);
    refreshList();
  }
}

/* Guard the generic short-range BH-BH merger (mergeBHs, section 10b):
   a pair bound in binaries[] is owned by updateBinaries(), which runs
   right AFTER updateInteractions() every frame and produces the full
   kilonova + relativistic jets + "Merger Remnant (BH)" sequence. Without
   this guard the pair would be collapsed early into the plain "Merged
   Black Hole" outcome before the binary engine could fire. Individually
   placed black holes are untouched and still merge through the original
   path exactly as before. */
var _origMergeBHs = mergeBHs;
mergeBHs = function (a, c) {
  var bound = binaries.some(function (bn) {
    return (bn.a === a && bn.b === c) || (bn.a === c && bn.b === a);
  });
  if (bound) return;
  _origMergeBHs(a, c);
};

/* ------------------------------------------------------------------ */
/* 15. Click-to-Inspect Details Panel                                 */
/* ------------------------------------------------------------------ */
const detailsEl = document.getElementById("details");
const detailsTitle = document.getElementById("dTitle");
const detailsBody = document.getElementById("dBody");
document.getElementById("dClose").addEventListener("click", () => { detailsEl.classList.add("hidden"); });

function showDetails(html) {
  detailsEl.classList.remove("hidden");
  detailsBody.innerHTML = html;
}
function fmtSci(v, unit) {
  if (Math.abs(v) < 0.001 || Math.abs(v) > 1e6) return v.toExponential(2) + (unit ? " " + unit : "");
  return v.toFixed(4) + (unit ? " " + unit : "");
}

function inspectFabric() {
  detailsTitle.textContent = "Spacetime Fabric";
  showDetails(
    '<div class="dCat">Einstein Field Equations</div>' +
    '<div class="dTxt">The fabric represents spacetime itself. Einstein\'s field equations relate the curvature of spacetime to the energy-momentum content:</div>' +
    '<div class="dEq">Gμν + Λgμν = (8πG/c⁴) Tμν</div>' +
    '<div class="dTxt">Here, <i>Gμν</i> is the Einstein tensor encoding curvature, <i>Tμν</i> is the stress-energy tensor, and <i>Λ</i> is the cosmological constant.</div>' +
    '<div class="dCat">Flamm Embedding</div>' +
    '<div class="dTxt">The grid-sheet view is a Flamm paraboloid — a 2D surface embedded in 3D whose shape matches the spatial geometry of the Schwarzschild metric. The depth at each point equals the proper radial distance from the flat-space value.</div>' +
    '<div class="dCat">5D Metric Ansatz</div>' +
    '<div class="dEq">ds² = −A(r)c²dt² + B(r)dr² + r²dΩ² + D(r)dw²</div>' +
    '<div class="dTxt">An extra spatial dimension <i>w</i> is compactified. Its size <i>D(r)</i> opens near massive objects via the threshold function, revealing the hidden fourth spatial dimension.</div>' +
    '<div class="dCat">Current Parameters</div>' +
    '<div class="dRow"><span class="dLbl">n (steepness)</span><span class="dVal">' + CONFIG.metric.n.toFixed(1) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">Φ₀ (threshold)</span><span class="dVal">' + CONFIG.metric.phi0.toFixed(3) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">α (coupling)</span><span class="dVal">' + CONFIG.metric.alpha.toFixed(3) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">ℓ (W-size)</span><span class="dVal">' + CONFIG.metric.ell.toFixed(1) + ' km</span></div>' +
    '<div class="dCat">Observational Context</div>' +
    '<div class="dTxt">The Flamm paraboloid was introduced in 1916 by Paul Flamm as the first embedding diagram of curved spacetime. It remains the standard visualization for Schwarzschild geometry in general-relativity textbooks.</div>'
  );
}

function inspectStar(body) {
  const M = body.GM * 1000;   // rough solar-mass scaling
  const rs = 2 * body.GM;
  const T_H = hawkingTemp(body.GM * 0.001);
  detailsTitle.textContent = body.name;
  showDetails(
    '<div class="dCat">Physical Properties</div>' +
    '<div class="dRow"><span class="dLbl">Type</span><span class="dVal">' + (body.type === "sun" ? "Main-sequence star (1 M☉)" : body.type === "star" ? "Heavy star (intermediate mass)" : body.type) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">Mass</span><span class="dVal">' + M.toFixed(2) + ' × 10⁻³ (sim)</span></div>' +
    '<div class="dRow"><span class="dLbl">Δ (Lucky)</span><span class="dVal">' + fmtDelta(readDelta(body)) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">D(r)/ℓ²</span><span class="dVal">' + (1 + CONFIG.metric.alpha * Math.pow(Math.max(body.warpGM / CONFIG.metric.phi0, 0), CONFIG.metric.n) / (1 + Math.pow(Math.max(body.warpGM / CONFIG.metric.phi0, 0), CONFIG.metric.n))).toFixed(6) + '</span></div>' +
    '<div class="dCat">Equations</div>' +
    '<div class="dEq">r_s = 2GM/c² = ' + rs.toFixed(4) + ' (sim units)\n' +
    'Φ = GM/(c²r) = ' + (body.warpGM).toFixed(4) + '/r\nθ_Lucky = (4GM/c²b)(1 + Δ)</div>' +

    '<div class="dTxt">For a normal star, <i>Φ ≪ Φ₀</i> at all distances, so Δ ≈ 0 and the fabric stays essentially flat. The extra deflection is of order 10⁻²⁸ to 10⁻³⁴ — safely within the Solar System\'s classical tests.</div>' +
    '<div class="dCat">History</div>' +
    '<div class="dTxt">Stars spend ~90% of their lives on the main sequence, fusing hydrogen into helium. Our Sun is a G-type main-sequence star, ~4.6 billion years old, roughly halfway through its main-sequence lifetime.</div>'
  );
}

function inspectBlackHole(body) {
  const T_H = hawkingTemp(body.GM * 0.001);
  const lambda_peak = hawkingWavelength(T_H);
  const L = hawkingPower(body.GM * 0.001);
  detailsTitle.textContent = body.name;
  showDetails(
    '<div class="dCat">Event Horizon</div>' +
    '<div class="dRow"><span class="dLbl">Horizon radius</span><span class="dVal">' + (2 * body.GM).toFixed(3) + ' (sim)</span></div>' +
    '<div class="dRow"><span class="dLbl">Surface gravity κ</span><span class="dVal">' + (1 / (4 * body.GM)).toFixed(4) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">Δ (Lucky)</span><span class="dVal">' + fmtDelta(readDelta(body)) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">D(r)/ℓ²</span><span class="dVal">' + (1 + CONFIG.metric.alpha * Math.pow(Math.max(body.warpGM * body.strength * CONFIG.visual.warpMul / CONFIG.metric.phi0, 0), CONFIG.metric.n) / (1 + Math.pow(Math.max(body.warpGM * body.strength * CONFIG.visual.warpMul / CONFIG.metric.phi0, 0), CONFIG.metric.n))).toFixed(4) + ' (threshold open)</span></div>' +
    '<div class="dCat">Hawking Radiation</div>' +
    '<div class="dEq">T_H = ℏc³/(8πGMk_B)\n' +
    'T_H ≈ ' + fmtSci(T_H, 'K') + '\nλ_peak = ' + fmtSci(lambda_peak, 'm') + '\nL ≈ ' + fmtSci(L, 'W') + '</div>' +
    '<div class="dTxt">Hawking radiation is quantum particle creation near the event horizon. For a solar-mass BH, T_H ≈ 60 nK — far below the CMB. Only micro black holes would glow visibly.</div>' +
    '<div class="dCat">Lucky Model</div>' +
    '<div class="dEq">D(r) = ℓ²[1 + α(Φ/Φ₀)ⁿ/(1+(Φ/Φ₀)ⁿ)]\n' +
    'Φ = GM/(c²r)\nShadow enlargement: 1–3.5%</div>' +
    '<div class="dTxt">Near a black hole, the gravitational potential Φ exceeds the threshold Φ₀, opening the extra dimension. This produces a controlled enlargement of the apparent shadow without violating Solar System constraints.</div>' +
    '<div class="dCat">Singularity</div>' +
    '<div class="dTxt">Classically, matter collapses to a point singularity of infinite density. Quantum gravity (string theory, loop quantum gravity) is expected to resolve this singularity, but no complete theory exists yet.</div>'
  );
}

function inspectNeutronStar(body) {
  const T_H = hawkingTemp(body.GM * 0.001);
  detailsTitle.textContent = body.name;
  showDetails(
    '<div class="dCat">Physical Properties</div>' +
    '<div class="dRow"><span class="dLbl">Type</span><span class="dVal">Neutron Star</span></div>' +
    '<div class="dRow"><span class="dLbl">Radius</span><span class="dVal">~10–12 km</span></div>' +
    '<div class="dRow"><span class="dLbl">Density</span><span class="dVal">~10¹⁷ kg/m³</span></div>' +
    '<div class="dRow"><span class="dLbl">B-field</span><span class="dVal">~10⁸–10¹⁵ T</span></div>' +
    '<div class="dRow"><span class="dLbl">Δ (Lucky)</span><span class="dVal">' + fmtDelta(readDelta(body)) + '</span></div>' +
    '<div class="dCat">Equations</div>' +
    '<div class="dEq">TOV limit: M ≲ 2.17 M☉\n' +
    'ρ_core ≈ 10¹⁷ kg/m³\nMagnetic dipole: B ∝ P⁻²\nθ_extra = (4GM/c²b)·Δ ≈ 4–9%</div>' +
    '<div class="dCat">Equation of State</div>' +
    '<div class="dTxt">The NS interior is governed by the nuclear equation of state — how pressure varies with density above nuclear saturation. Different EoS models predict different maximum masses and radii. NICER X-ray data constrains the radius to ~12 km for a 1.4 M☉ NS.</div>' +
    '<div class="dCat">Lucky Model</div>' +
    '<div class="dTxt">At neutron-star gravitational potentials, Φ passes the threshold Φ₀, opening D(r). The extra deflection Δ ≈ 4–9% is within the allowed window and produces clear tesseract-like W-edge extrusion in the fabric.</div>'
  );
}

function inspectPulsar(body) {
  inspectNeutronStar(body);
  detailsTitle.textContent = "Pulsar (" + body.name + ")";
  detailsBody.innerHTML +=
    '<div class="dCat">Pulsar-Specific Properties</div>' +
    '<div class="dRow"><span class="dLbl">Spin rate</span><span class="dVal">~ms to seconds</span></div>' +
    '<div class="dRow"><span class="dLbl">Frame dragging</span><span class="dVal">Visible in fabric</span></div>' +
    '<div class="dCat">Frame-Dragging</div>' +
    '<div class="dTxt">The pulsar\'s extreme rotation generates gravitomagnetic frame-dragging (Lense-Thirring effect). The fabric around it is sheared and twisted helically, synchronised with the spin. This is a unique signature distinguishable from a non-spinning NS.</div>' +
    '<div class="dEq">Ω_LT = 2GJ/(c²r³)\n' +
    'where J = Iω is the angular momentum</div>';
}

function inspectLight() {
  detailsTitle.textContent = "Light / Photon Trajectory";
  showDetails(
    '<div class="dCat">Null Geodesics</div>' +
    '<div class="dEq">ds² = 0 (null condition)\n' +
    'd²x^μ/dλ² + Γ^μ_αβ (dx^α/dλ)(dx^β/dλ) = 0</div>' +
    '<div class="dTxt">Light always travels in perfectly straight lines in the full 5D geometry. The observed bending is purely a projection effect — the opening of D(r) makes the straight 5D path appear curved when projected into our 3D view.</div>' +
    '<div class="dCat">Lucky Deflection Formula</div>' +
    '<div class="dEq">θ_Lucky = (4GM/c²b)(1 + Δ)\nΔ = 0.90·α·(Φ_b/Φ₀)ⁿ / (1+(Φ_b/Φ₀)ⁿ)\nb = impact parameter</div>' +
    '<div class="dTxt">Near ordinary stars: extra deflection ≈ 10⁻³³ (invisible). Near neutron stars: Δ ≈ 4–9% excess. Near black holes: shadow enlargement 1–3.5%.</div>' +
    '<div class="dCat">Gravitational Redshift</div>' +
    '<div class="dEq">z = 1/√(A(r)) − 1\n' +
    'A(r) = 1 − 2GM/(c²r)</div>' +
    '<div class="dTxt">Photons climbing out of a gravitational well lose energy and are redshifted. This effect is measured routinely on Earth (Pound-Rebka experiment, 1959) and is critical for GPS satellite clock corrections.</div>'
  );
}

function inspectPlanet(body) {
  detailsTitle.textContent = body.name || "Planet";
  showDetails(
    '<div class="dCat">Orbital Properties</div>' +
    '<div class="dRow"><span class="dLbl">Mass (sim)</span><span class="dVal">' + (body.gm || 0).toExponential(2) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">Position</span><span class="dVal">' + (body.worldPos || new THREE.Vector3()).toArray().map(function(v) { return v.toFixed(2); }).join(', ') + '</span></div>' +
    '<div class="dCat">Geodesic Motion</div>' +
    '<div class="dEq">d²x^μ/dτ² + Γ^μ_αβ (dx^α/dτ)(dx^β/dτ) = 0</div>' +
    '<div class="dTxt">Planets follow timelike geodesics — the straightest possible paths through curved spacetime. Their orbital curvature is determined by the effective potential of the 5D metric, including the (1+Δ) correction from the Lucky Model.</div>' +
    '<div class="dCat">Why They Orbit</div>' +
    '<div class="dTxt">An object with tangential velocity in a gravitational field follows a curved path — not because of a "force" pulling it, but because spacetime itself is curved. The planet is moving in a straight line through curved geometry.</div>'
  );
}

function inspectMergerRemnant(body) {
  detailsTitle.textContent = body.name;
  showDetails(
    '<div class="dCat">Merger Remnant</div>' +
    '<div class="dRow"><span class="dLbl">Final mass</span><span class="dVal">' + (body.GM * 1000).toFixed(2) + ' × 10⁻³ (sim)</span></div>' +
    '<div class="dRow"><span class="dLbl">Δ (Lucky)</span><span class="dVal">' + fmtDelta(readDelta(body)) + '</span></div>' +
    '<div class="dRow"><span class="dLbl">D(r)/ℓ²</span><span class="dVal">Threshold ' + (readDelta(body) > 0.01 ? 'OPEN' : 'closed') + '</span></div>' +
    '<div class="dCat">Formation</div>' +
    '<div class="dTxt">This remnant formed from the collision of two compact objects. If the total mass exceeds the Tolman-Oppenheimer-Volkoff limit (~2.17 M☉), the remnant collapses into a black hole. Below TOV, a hypermassive neutron star persists temporarily before potentially collapsing.</div>' +
    '<div class="dEq">TOV limit ≈ 2.17 M☉\nKilonova: r-process nucleosynthesis\nGravitational wave peak: f_GW ≈ 1–2 kHz</div>' +
    '<div class="dCat">Ring-Down</div>' +
    '<div class="dTxt">After the merger, the remnant settles via quasi-normal mode oscillations — gravitational "ring-down" waves that encode the remnant\'s mass and spin. These were first detected by LIGO on September 14, 2015 (GW150914).</div>'
  );
}

function inspectHawkingRegion() {
  detailsTitle.textContent = "Hawking Radiation Zone";
  showDetails(
    '<div class="dCat">Hawking Radiation</div>' +
    '<div class="dEq">T_H = ℏc³/(8πGMk_B)\n' +
    'T_H ∝ 1/M\nL = ℏc⁶/(15360πG²M²)\nλ_peak = 2.898×10⁻³/T</div>' +
    '<div class="dTxt">Quantum field theory in curved spacetime predicts that black holes emit thermal radiation at the Hawking temperature. Particle-antiparticle pairs are created near the event horizon; one falls in (negative energy) and the other escapes as real radiation.</div>' +
    '<div class="dCat">Evaporation</div>' +
    '<div class="dTxt">As the BH radiates, it loses mass: dM/dt = −L/c². Smaller BHs are hotter and radiate faster, leading to runaway evaporation. A solar-mass BH would take ~10⁶⁷ years to evaporate — far longer than the age of the universe (1.4×10¹⁰ years). A primordial micro-BH (~10¹² kg) would explode now.</div>' +
    '<div class="dCat">Thermal Distribution</div>' +
    '<div class="dTxt">The radiation is exactly thermal (blackbody) at temperature T_H. Intensity falls with distance as 1/r². The glow is higher for smaller (hotter) black holes and almost imperceptible for stellar-mass ones.</div>'
  );
}

/* Intercept pickAt to also open the details panel */
var _origPickAt = pickAt;
pickAt = function(e) {
  _origPickAt(e);
  if (selected) {
    if (selected.name && (selected.name.indexOf("Merger") !== -1 || selected.name.indexOf("Remnant") !== -1)) inspectMergerRemnant(selected);
    else if (selected.type === "bh") inspectBlackHole(selected);
    else if (selected.type === "pulsar") inspectPulsar(selected);
    else if (selected.type === "ns") inspectNeutronStar(selected);
    else if (selected.type === "star") inspectStar(selected);
    else if (selected.type === "sun") inspectStar(selected);
    else if (selected.name && selected.name.indexOf("meteor") !== -1) {
      detailsTitle.textContent = "Meteor";
      showDetails(
        '<div class="dCat">Properties</div>' +
        '<div class="dRow"><span class="dLbl">Mass (sim)</span><span class="dVal">' + (selected.gm || 0).toExponential(2) + '</span></div>' +
        '<div class="dRow"><span class="dLbl">Position</span><span class="dVal">' + (selected.worldPos || new THREE.Vector3()).toArray().map(function(v) { return v.toFixed(2); }).join(', ') + '</span></div>' +
        '<div class="dCat">Geodesic Motion</div>' +
        '<div class="dTxt">Meteors follow geodesics determined by the combined gravitational potential of all massive bodies. Near black holes, they can be captured or torn apart by tidal forces.</div>'
      );
    } else {
      /* clicked on a planet in a solar system */
      if (selected.mesh && selected.vel) inspectPlanet(selected);
    }
  } else {
    /* clicked on empty space — inspect the fabric */
    inspectFabric();
  }
};

/* ------------------------------------------------------------------ */
/* 16. UI wiring — new buttons + evaporation toggle                    */
/* ------------------------------------------------------------------ */
document.getElementById("bNSBinary").addEventListener("click", function() { enterPlacement("nsbinary"); });
document.getElementById("bBHBinary").addEventListener("click", function() { enterPlacement("bhbinary"); });
document.getElementById("sEvap").addEventListener("change", function() { evapEnabled.value = document.getElementById("sEvap").checked; });

/* patch placeObject to handle nsbinary */
var _origPlaceObject = placeObject;
placeObject = function(type, p) {
  if (type === "nsbinary") { placeNSBinary(p); return; }
  if (type === "bhbinary") { placeBHBinary(p); return; }
  _origPlaceObject(type, p);
};

/* patch updateBodies to include new systems */
var _origUpdateBodies = updateBodies;
updateBodies = function(dt) {
  _origUpdateBodies(dt);
  updateBinaries(dt);
  updateHawking(dt);
};

/* If the cover asked for a specific first view (the "Jump to the 5D
   Fabric" button opens the cubic lattice directly), apply it now that
   the scene exists — and clear it so later boots fall back to sheet. */
if (window.__coverLaunchView) { setView(window.__coverLaunchView); window.__coverLaunchView = null; }
window.__simReady = true;   // lets the cover skip the loader on re-entry

}  /* ---- end bootSimulator() (deferred until the cover CTA) ---- */

/* ------------------------------------------------------------------ */
/* 17. Cover-page reveal — single-file navigation                     */
/* ------------------------------------------------------------------ */
/* Same-page navigation, no reload / hash / location change (§4.2):
   the CTA fades #coverPage out, re-shows the #overlay spinner as the
   three.js loading screen while the scene warms up, and boots the
   simulator exactly once (idempotent launcher, §4.1 defer). */
window.__launchSimulator = function () {
  if (simBooted) return;
  simBooted = true;
  bootSimulator();
};

var _coverEl = document.getElementById("coverPage");
/* every element with .cvEnter launches the simulation (hero CTA, outro CTA) */
var _enterBtns = document.querySelectorAll("#coverPage .cvEnter");
var _simPausedByBack = false;
function _togglePause() {
  window.dispatchEvent(new KeyboardEvent("keydown", { code: "KeyP", key: "p", bubbles: true }));
  window.dispatchEvent(new KeyboardEvent("keyup", { code: "KeyP", key: "p", bubbles: true }));
}
function _startSimulation(view) {
  window.__coverLaunchView = view || null;   // e.g. "cubic" from the 5D-fabric jump button
  if (_simPausedByBack) { _togglePause(); _simPausedByBack = false; }   // wake the scene again
  _coverEl.classList.add("leaving");
  if (window.__simReady) {
    document.getElementById("overlay").style.display = "none";   // already warm — skip the loader
  } else {
    document.getElementById("overlay").style.display = "flex";   // visible loader under the fade
    window.__launchSimulator();
  }
  if (window.__stopCoverStars) window.__stopCoverStars();
  setTimeout(function () {                                       // drop the cover out of the hit-test path
    _coverEl.style.display = "none";
  }, 800);
}
for (var _bi = 0; _bi < _enterBtns.length; _bi++) {
  (function (btn) {
    btn.addEventListener("click", function () {
      _startSimulation(btn.getAttribute("data-view") || null);
    });
  })(_enterBtns[_bi]);
}

/* --- in-simulator "Back to Base-1" — lift the cover back up --- */
var _backBtn = document.getElementById("bBackBase");
if (_backBtn) {
  _backBtn.addEventListener("click", function () {
    _coverEl.style.display = "";                       // unhide the cover (still fades from its .leaving state)
    var sc = _coverEl.querySelector(".cvScroll");
    if (sc) sc.scrollTop = 0;                          // land on the hero again
    if (window.__startCoverStars) window.__startCoverStars();
    void _coverEl.offsetWidth;                         // restart the CSS transition
    _coverEl.classList.remove("leaving");
    if (!_simPausedByBack) { _togglePause(); _simPausedByBack = true; }   // rest the scene behind the cover
  });
}

/* Cover space backdrop (v2) — a live 2D-canvas sky, vanilla JS, no
   three.js: gold-haze nebulas that drift, a layered parallax starfield,
   slowly rising gold dust motes and the occasional shooting star.
   Cheap (two fills per star, sprite blits for the nebulas) and cancelled
   once the cover is dismissed so it never competes with the simulator's
   frame budget. */
(function () {
  var cvs = document.getElementById("coverStars");
  if (!cvs) return;
  var ctx = cvs.getContext("2d");
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var DPR = Math.min(2, window.devicePixelRatio || 1);
  var W = 0, H = 0;
  var far = [], near = [], motes = [], meteors = [], nebulas = [];
  var raf = 0, running = true, last = 0;
  var px = 0, py = 0, tx = 0, ty = 0;       // parallax: eased toward pointer
  var meteorTimer = 1.2;

  function nebulaSprite(r, g, b) {
    var s = document.createElement("canvas"); s.width = s.height = 256;
    var c = s.getContext("2d");
    var gr = c.createRadialGradient(128, 128, 0, 128, 128, 128);
    gr.addColorStop(0, "rgba(" + r + "," + g + "," + b + ",0.50)");
    gr.addColorStop(0.35, "rgba(" + r + "," + g + "," + b + ",0.16)");
    gr.addColorStop(1, "rgba(" + r + "," + g + "," + b + ",0)");
    c.fillStyle = gr; c.fillRect(0, 0, 256, 256);
    return s;
  }
  function mkStar(depth) {
    var gold = Math.random() < 0.3;
    return { x: Math.random(), y: Math.random(),
      r: (0.3 + Math.random() * depth * 1.5) * DPR,
      a: 0.05 + Math.random() * 0.4,
      tw: 0.3 + Math.random() * 1.6, ph: Math.random() * 6.283,
      col: gold ? "232,201,136" : "238,242,252" };
  }
  function seed() {
    var n = Math.max(90, Math.min(210, Math.round(W * H / 9500)));
    far = []; near = []; motes = [];
    for (var i = 0; i < n; i++) far.push(mkStar(0.55));
    for (var j = 0; j < Math.floor(n * 0.5); j++) near.push(mkStar(1));
    for (var k = 0; k < 24; k++) motes.push({ x: Math.random() * W, y: Math.random() * H,
      r: (0.9 + Math.random() * 1.8) * DPR, a: 0.1 + Math.random() * 0.34,
      vx: (0.05 + Math.random() * 0.09) * DPR, vy: (0.01 + Math.random() * 0.035) * DPR,
      ph: Math.random() * 6.283, tw: 0.3 + Math.random() * 1.2 });
    nebulas = [
      { s: nebulaSprite(212, 175, 55),  fx: 0.5, fy: -0.08, size: 1.7, a: 0.55, p: 0 },
      { s: nebulaSprite(255, 240, 205), fx: 0.12, fy: 0.8, size: 1.15, a: 0.38, p: 2.1 },
      { s: nebulaSprite(190, 160, 90),  fx: 0.9, fy: 0.35, size: 1.25, a: 0.42, p: 4.2 }
    ];
  }
  function resize() {
    W = cvs.width = Math.floor(window.innerWidth * DPR);
    H = cvs.height = Math.floor(window.innerHeight * DPR);
    seed();
  }
  function drawStars(list, depth, t) {
    for (var i = 0; i < list.length; i++) {
      var s = list[i];
      var k = 0.5 + 0.5 * Math.sin(t * 0.0005 * s.tw + s.ph);
      ctx.globalAlpha = s.a * k;
      ctx.fillStyle = "rgba(" + s.col + ",1)";
      ctx.beginPath();
      ctx.arc(s.x * W + px * 22 * depth, s.y * H + py * 14 * depth, s.r, 0, 6.2832);
      ctx.fill();
    }
  }
  function spawnMeteor() {
    var left = Math.random() < 0.5;
    var speed = H * (0.28 + Math.random() * 0.3);
    meteors.push({ x: left ? -40 : W + 40,
      y: H * (0.05 + Math.random() * 0.4),
      vx: (left ? 1 : -1) * speed * 0.7, vy: speed * 0.7, trail: [], life: 1.1 });
  }
  function drawMeteors(dt, t) {
    meteorTimer -= dt;
    if (!reduced && meteorTimer <= 0) { spawnMeteor(); meteorTimer = 1.8 + Math.random() * 3.6; }
    for (var i = meteors.length - 1; i >= 0; i--) {
      var m = meteors[i];
      m.life -= dt; m.x += m.vx * dt; m.y += m.vy * dt;
      m.trail.push({ x: m.x, y: m.y });
      if (m.trail.length > 9) m.trail.shift();
      for (var s2 = 0; s2 < m.trail.length - 1; s2++) {
        var f = s2 / m.trail.length;
        ctx.globalAlpha = Math.min(1, m.life) * (0.5 * (1 - f));
        ctx.strokeStyle = "rgba(" + (s2 === m.trail.length - 2 ? "255,248,228" : "232,201,136") + ",1)";
        ctx.lineWidth = Math.max(0.4, 1.8 * (1 - f)) * DPR;
        ctx.beginPath();
        ctx.moveTo(m.trail[s2].x, m.trail[s2].y);
        ctx.lineTo(m.trail[s2 + 1].x, m.trail[s2 + 1].y);
        ctx.stroke();
      }
      if (m.life <= 0 || m.x < -160 || m.x > W + 160 || m.y > H + 120) meteors.splice(i, 1);
    }
  }
  function frame(t) {
    if (!running) return;
    if (!W || !H) resize();   // cover may boot before the iframe is sized
    var dt = last ? Math.min(0.05, (t - last) / 1000) : 0.016;
    last = t;
    px += (tx - px) * 0.03; py += (ty - py) * 0.03;
    ctx.clearRect(0, 0, W, H);
    ctx.globalAlpha = 1;
    /* drifting nebula haze */
    for (var i = 0; i < nebulas.length; i++) {
      var nb = nebulas[i];
      var st = t * 0.00006 + nb.p;
      var cx = (nb.fx + Math.sin(st) * 0.05) * W;
      var cy = (nb.fy + Math.cos(st * 0.7) * 0.04) * H;
      var sz = nb.size * Math.min(W, H);
      ctx.globalAlpha = nb.a;
      ctx.drawImage(nb.s, cx - sz / 2, cy - sz / 2, sz, sz);
    }
    ctx.globalAlpha = 1;
    drawStars(far, 0.35, t);
    drawStars(near, 0.75, t);
    /* rising gold dust */
    for (var j = 0; j < motes.length; j++) {
      var mo = motes[j];
      mo.x += mo.vx * dt + Math.sin(t * 0.0003 + mo.ph) * 0.02 * DPR;
      mo.y -= mo.vy * dt;
      if (mo.y < -8) { mo.y = H + 8; mo.x = Math.random() * W; }
      if (mo.x > W + 8) mo.x = -8;
      var tw = 0.55 + 0.45 * Math.sin(t * 0.0008 * mo.tw + mo.ph);
      ctx.globalAlpha = mo.a * tw;
      ctx.fillStyle = "rgba(232,201,136,1)";
      ctx.beginPath(); ctx.arc(mo.x, mo.y, mo.r, 0, 6.2832); ctx.fill();
    }
    ctx.globalAlpha = 1;
    drawMeteors(dt, t);
    raf = requestAnimationFrame(frame);
  }
  window.addEventListener("resize", resize);
  window.addEventListener("pointermove", function (e) {
    tx = (e.clientX / (window.innerWidth || 1)) * 2 - 1;
    ty = (e.clientY / (window.innerHeight || 1)) * 2 - 1;
  }, { passive: true });
  resize();
  raf = requestAnimationFrame(frame);
  window.__stopCoverStars = function () { running = false; if (raf) cancelAnimationFrame(raf); };
  window.__startCoverStars = function () {
    if (running) return;
    running = true; last = 0; meteorTimer = 1.2;
    raf = requestAnimationFrame(frame);
  };
})();

/* Scroll-reveal staging + smooth-scroll cue for the cover acts */
(function () {
  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var els = document.querySelectorAll("#coverPage .reveal");
  function show(el) { el.classList.add("in"); }
  if (!("IntersectionObserver" in window)) {
    for (var i = 0; i < els.length; i++) show(els[i]);
  } else {
    var io = new IntersectionObserver(function (entries) {
      for (var j = 0; j < entries.length; j++) {
        if (entries[j].isIntersecting) { show(entries[j].target); io.unobserve(entries[j].target); }
      }
    }, { threshold: 0.1, rootMargin: "0px 0px -6% 0px" });
    for (var k = 0; k < els.length; k++) io.observe(els[k]);
  }
  var cue = document.querySelector("#coverPage .cvCue");
  function cueGo(e) {
    if (e.type === "keydown" && e.key !== "Enter" && e.key !== " ") return;
    e.preventDefault();
    var target = document.getElementById("cvWhat");
    if (target) target.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
  }
  if (cue) { cue.addEventListener("click", cueGo); cue.addEventListener("keydown", cueGo); }
})();
</script>
</body>
</html>
