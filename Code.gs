const SHEET_NAME = 'Leaderboard';

function doGet() {
  const sheet = getSheet_();
  const values = sheet.getDataRange().getValues().slice(1);
  const rows = values
    .filter(row => row[0] && row[1] !== '')
    .map(row => ({ name: row[0], score: Number(row[1]) || 0 }))
    .sort((a, b) => b.score - a.score)
    .slice(0, 8);

  return ContentService
    .createTextOutput(JSON.stringify(rows))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  const sheet = getSheet_();
  const payload = JSON.parse(e.postData.contents || '{}');
  const name = String(payload.name || 'Player').slice(0, 18);
  const score = Number(payload.score || 0);
  sheet.appendRow([name, score, new Date()]);

  return ContentService
    .createTextOutput(JSON.stringify({ ok: true }))
    .setMimeType(ContentService.MimeType.JSON);
}

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow(['Name', 'Score', 'Created At']);
  }
  return sheet;
}
