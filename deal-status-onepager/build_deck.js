// Builds the U.S. Investment Accelerator deal-status one-pager (letter landscape PPTX template).
const pptxgen = require("pptxgenjs");

const C = {
  navy: "0D366B", gold: "B8933F",
  ink: "0B0B0B", ink2: "52514E", muted: "898781",
  hairline: "E1E0D9", strip: "F6F5F2",
  headerSub: "C9D7EC", chip: "FFD9A8",
  jpRed: "BC002D", krBlue: "003478", krRed: "C60C30",
  annDot: "0CA30C", annBg: "E7F3E7", annTx: "006300",
  actDot: "2A78D6", actBg: "E5EEFB", actTx: "1C5CAB",
  conDot: "898781", conBg: "F0EFEC", conTx: "52514E",
};
const FONT = "Arial";

const STAGE = {
  ann: { label: "Announced",    dot: C.annDot, bg: C.annBg, tx: C.annTx, w: 0.96 },
  act: { label: "Active",       dot: C.actDot, bg: C.actBg, tx: C.actTx, w: 0.76 },
  con: { label: "Consultation", dot: C.conDot, bg: C.conBg, tx: C.conTx, w: 1.08 },
};

const pres = new pptxgen();
pres.defineLayout({ name: "LETTER_L", width: 11, height: 8.5 });
pres.layout = "LETTER_L";
const slide = pres.addSlide();
slide.background = { color: "FFFFFF" };

// ---------- header band ----------
slide.addShape(pres.ShapeType.rect, { x: 0, y: 0, w: 11, h: 1.05, fill: { color: C.navy }, line: { type: "none" } });
slide.addShape(pres.ShapeType.rect, { x: 0, y: 1.05, w: 11, h: 0.035, fill: { color: C.gold }, line: { type: "none" } });
slide.addText("U.S. INVESTMENT ACCELERATOR  ·  U.S. DEPARTMENT OF COMMERCE", {
  x: 0.42, y: 0.17, w: 7.6, h: 0.24, margin: 0,
  fontFace: FONT, fontSize: 9.5, bold: true, color: C.headerSub, charSpacing: 3,
});
slide.addText("Investment Deal Portfolio — Status Overview", {
  x: 0.40, y: 0.45, w: 7.8, h: 0.46, margin: 0,
  fontFace: FONT, fontSize: 25, bold: true, color: "FFFFFF",
});
slide.addShape(pres.ShapeType.roundRect, {
  x: 8.12, y: 0.355, w: 2.48, h: 0.34, rectRadius: 0.05,
  fill: { type: "none" }, line: { color: C.chip, width: 1 },
});
slide.addText("PRE-DECISIONAL · INTERNAL USE", {
  x: 8.12, y: 0.355, w: 2.48, h: 0.34, margin: 0, align: "center", valign: "middle",
  fontFace: FONT, fontSize: 7.5, bold: true, color: C.chip, charSpacing: 1.2,
});

// ---------- summary strip ----------
slide.addShape(pres.ShapeType.rect, { x: 0, y: 1.085, w: 11, h: 1.06, fill: { color: C.strip }, line: { type: "none" } });
slide.addShape(pres.ShapeType.rect, { x: 0, y: 2.145, w: 11, h: 0.01, fill: { color: C.hairline }, line: { type: "none" } });
for (const dx of [1.75, 3.95, 6.20, 8.25]) {
  slide.addShape(pres.ShapeType.rect, { x: dx, y: 1.27, w: 0.008, h: 0.72, fill: { color: C.hairline }, line: { type: "none" } });
}

function tileLabel(x, w, text) {
  slide.addText(text, {
    x, y: 1.25, w, h: 0.2, margin: 0,
    fontFace: FONT, fontSize: 8, bold: true, color: C.muted, charSpacing: 1.5,
  });
}
function flagJP(x, y, w, h) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.02, fill: { color: "FFFFFF" }, line: { color: "D5D3CC", width: 0.75 } });
  const d = h * 0.56;
  slide.addShape(pres.ShapeType.ellipse, { x: x + (w - d) / 2, y: y + (h - d) / 2, w: d, h: d, fill: { color: C.jpRed }, line: { type: "none" } });
}
function flagKR(x, y, w, h) {
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.02, fill: { color: "FFFFFF" }, line: { color: "D5D3CC", width: 0.75 } });
  const d = h * 0.56;
  const cx = x + (w - d) / 2, cy = y + (h - d) / 2;
  slide.addShape(pres.ShapeType.ellipse, { x: cx, y: cy, w: d, h: d, fill: { color: C.krBlue }, line: { type: "none" } });
  slide.addShape(pres.ShapeType.pie, { x: cx, y: cy, w: d, h: d, angleRange: [180, 360], fill: { color: C.krRed }, line: { type: "none" } });
}

// Tile 1 — total deals
tileLabel(0.42, 1.3, "TOTAL DEALS");
slide.addText("19", { x: 0.42, y: 1.47, w: 1.3, h: 0.4, margin: 0, fontFace: FONT, fontSize: 19, bold: true, color: C.ink });

// Tile 2 — total value
tileLabel(1.98, 1.9, "TOTAL PORTFOLIO VALUE");
slide.addText("$XXX.X B", { x: 1.98, y: 1.47, w: 1.9, h: 0.4, margin: 0, fontFace: FONT, fontSize: 19, bold: true, color: C.ink });

// Tile 3 — Japan
flagJP(4.18, 1.25, 0.22, 0.155);
tileLabel(4.47, 1.6, "JAPAN-FUNDED");
slide.addText([
  { text: "13", options: { fontSize: 19, bold: true, color: C.ink } },
  { text: "  deals  ·  $XX B", options: { fontSize: 10.5, color: C.ink2 } },
], { x: 4.18, y: 1.47, w: 1.95, h: 0.4, margin: 0, fontFace: FONT });

// Tile 4 — Korea
flagKR(6.43, 1.25, 0.22, 0.155);
tileLabel(6.72, 1.5, "KOREA-FUNDED");
slide.addText([
  { text: "6", options: { fontSize: 19, bold: true, color: C.ink } },
  { text: "  deals  ·  $XX B", options: { fontSize: 10.5, color: C.ink2 } },
], { x: 6.43, y: 1.47, w: 1.8, h: 0.4, margin: 0, fontFace: FONT });

// Tile 5 — pipeline by stage (order matches the tables: Announced, Consultation, Active)
tileLabel(8.48, 2.1, "PIPELINE BY STAGE");
const pipe = [
  ["6", STAGE.ann], ["6", STAGE.con], ["7", STAGE.act],
];
pipe.forEach(([n, st], i) => {
  slide.addText([
    { text: "● ", options: { fontSize: 8, color: st.dot } },
    { text: n + "  ", options: { fontSize: 10, bold: true, color: C.ink } },
    { text: st.label, options: { fontSize: 9.5, color: C.ink2 } },
  ], { x: 8.48, y: 1.485 + i * 0.215, w: 2.1, h: 0.21, margin: 0, fontFace: FONT });
});

// ---------- country sections ----------
const headerCell = (t, opts = {}) => ({
  text: t,
  options: {
    fontFace: FONT, fontSize: 8, bold: true, color: C.muted, charSpacing: 1,
    valign: "middle", margin: [0.02, 0.03, 0.02, 0.03],
    border: [{ type: "none" }, { type: "none" }, { type: "solid", pt: 1.25, color: C.hairline }, { type: "none" }],
    ...opts,
  },
});
const dataCell = (t, opts = {}) => ({
  text: t,
  options: {
    fontFace: FONT, fontSize: 9.5, color: C.ink,
    valign: "middle", margin: [0.02, 0.03, 0.02, 0.03],
    border: [{ type: "none" }, { type: "none" }, { type: "solid", pt: 0.75, color: C.hairline }, { type: "none" }],
    ...opts,
  },
});

const ROW_H = 0.375;
const TABLE_Y = 2.81;

function countrySection({ x, w, colW, name, flag, accent, meta, rows, startNum, headerFontSize = 8, headerSpacing = 1 }) {
  flag(x, 2.365, 0.30, 0.205);
  slide.addText(name, { x: x + 0.38, y: 2.32, w: 1.6, h: 0.3, margin: 0, fontFace: FONT, fontSize: 14, bold: true, color: C.ink, charSpacing: 1 });
  slide.addText(meta, { x: x + w - 3.0, y: 2.375, w: 3.0, h: 0.22, margin: 0, align: "right", fontFace: FONT });
  slide.addShape(pres.ShapeType.rect, { x, y: 2.69, w, h: 0.028, fill: { color: accent }, line: { type: "none" } });

  const hOpts = { fontSize: headerFontSize, charSpacing: headerSpacing };
  const tableRows = [[
    headerCell("COMPANY", hOpts),
    headerCell("SECTOR", hOpts),
    headerCell("STAGE", hOpts),
    headerCell("DEAL SIZE", { ...hOpts, align: "right", margin: [0.02, 0.08, 0.02, 0.03] }),
    headerCell("OWNER’S REP", { ...hOpts, margin: [0.02, 0.03, 0.02, 0.06] }),
    headerCell("WARRANTS %", { ...hOpts, align: "right", margin: [0.02, 0.08, 0.02, 0.03] }),
  ]];
  rows.forEach((stKey, i) => {
    tableRows.push([
      dataCell(`Company ${startNum + i}`, { bold: true }),
      dataCell("Sector", { color: C.ink2, fontSize: 9 }),
      dataCell(""), // stage pill overlaid below
      dataCell("$X.X B", { align: "right", margin: [0.02, 0.10, 0.02, 0.03] }),
      dataCell("First Last", { color: C.ink2, margin: [0.02, 0.03, 0.02, 0.06] }),
      dataCell("X.X%", { align: "right", margin: [0.02, 0.10, 0.02, 0.03] }),
    ]);
  });
  slide.addTable(tableRows, {
    x, y: TABLE_Y, w, colW,
    rowH: [0.28, ...rows.map(() => ROW_H)],
    autoPage: false,
  });

  // stage pills over the Stage column
  rows.forEach((stKey, i) => {
    addPill(x + colW[0] + colW[1] + 0.05, TABLE_Y + 0.28 + i * ROW_H + (ROW_H - 0.24) / 2, STAGE[stKey]);
  });
}

function addPill(x, y, st, wOverride) {
  const w = wOverride || st.w;
  slide.addShape(pres.ShapeType.roundRect, { x, y, w, h: 0.24, rectRadius: 0.12, fill: { color: st.bg }, line: { type: "none" } });
  slide.addText([
    { text: "● ", options: { fontSize: 6.5, color: st.dot } },
    { text: st.label, options: { fontSize: 8, bold: true, color: st.tx } },
  ], { x, y, w, h: 0.24, margin: 0, align: "center", valign: "middle", fontFace: FONT });
}

const metaRuns = (deals, ph) => [
  { text: deals, options: { fontSize: 10, bold: true, color: C.ink } },
  { text: "  ·  " + ph, options: { fontSize: 10, color: C.ink2 } },
];

// Both tables identical width, sharing one column layout.
const TABLE_W = 4.93;
const COL_W = [0.91, 0.62, 1.14, 0.63, 0.82, 0.81];
countrySection({
  x: 0.42, w: TABLE_W, colW: COL_W,
  name: "JAPAN", flag: flagJP, accent: C.jpRed,
  meta: metaRuns("13 deals", "$XX.X B total"),
  rows: ["ann", "ann", "ann", "ann", "ann", "ann", "con", "con", "con", "act", "act", "act", "act"],
  startNum: 1,
  headerFontSize: 7, headerSpacing: 0,
});
countrySection({
  x: 5.65, w: TABLE_W, colW: COL_W,
  name: "KOREA", flag: flagKR, accent: C.krBlue,
  meta: metaRuns("6 deals", "$XX.X B total"),
  rows: ["con", "con", "con", "act", "act", "act"],
  startNum: 14,
  headerFontSize: 7, headerSpacing: 0,
});

// ---------- footer ----------
slide.addShape(pres.ShapeType.rect, { x: 0.42, y: 8.10, w: 10.16, h: 0.01, fill: { color: C.hairline }, line: { type: "none" } });
slide.addText("Data as of July 29, 2026", {
  x: 7.0, y: 8.16, w: 3.58, h: 0.2, margin: 0, align: "right", fontFace: FONT, fontSize: 7.5, color: C.muted,
});

// ---------- off-page helper (visible while editing, never prints) ----------
slide.addText("SPARE STAGE TAGS — copy (Ctrl/Cmd-drag) onto any row.\nThis area is off the page and never prints.", {
  x: 11.25, y: 2.5, w: 2.2, h: 0.55, margin: 0, fontFace: FONT, fontSize: 8, bold: true, color: C.muted,
});
addPill(11.25, 3.15, STAGE.ann);
addPill(11.25, 3.50, STAGE.con);
addPill(11.25, 3.85, STAGE.act);

slide.addNotes(
  "FILL-IN GUIDE\n" +
  "1. Type over every gray/placeholder value: Company 1-19, Sector, the $X.X B deal sizes (all in billions), First Last (owner's rep), X.X% (warrants), the summary tiles, and the two '$XX.X B total' figures next to JAPAN and KOREA.\n" +
  "2. Stage tags are already set to the plan: Japan = 6 Announced, 3 Consultation, 4 Active. Korea = 3 Consultation, 3 Active (none announced). To change one anyway, delete it and Ctrl/Cmd-drag a spare tag from the right of the page into place. The spares sit off the page and never print.\n" +
  "3. Add/remove rows: click in a table, use Table Layout > Insert/Delete Rows. If you change row counts, drag the tags to keep them aligned with their rows, and update the counts in the summary strip.\n" +
  "4. Rows are grouped by stage: Announced first, then Consultation, then Active.\n" +
  "5. Export for the meeting: File > Export/Save As > PDF. The page is exactly US Letter landscape, so it also prints 1:1."
);

pres.writeFile({ fileName: process.argv[2] || "US-Investment-Accelerator-Deal-Status.pptx" })
  .then((f) => console.log("wrote", f));
