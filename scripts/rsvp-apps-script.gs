/**
 * Yuki & Fellipe — RSVP Google Apps Script
 *
 * SETUP (about 5 minutes):
 * 1. Go to https://sheets.google.com and create a spreadsheet named "Yuki-Fellipe-RSVPs"
 * 2. Extensions → Apps Script → paste this entire file → Save
 * 3. Deploy → New deployment → Type: Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 4. Copy the Web App URL into js/main.js → RSVP_ENDPOINT = "YOUR_URL"
 * 5. Run setupTriggerOnce() once from the Apps Script editor
 *    (Authorize when prompted — this schedules the Excel email every 15 days)
 *
 * Emails go to: fellipe.theodoro@yahoo.com
 */

var EMAIL_TO = "fellipe.theodoro@yahoo.com";
var SHEET_NAME = "RSVPs";

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = getOrCreateSheet_();
    sheet.appendRow([
      new Date(),
      data.submittedAt || "",
      data.name || "",
      data.attending || "",
      data.guests || "",
      data.language || "",
    ]);
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

function doGet() {
  return json_({ ok: true, service: "Yuki & Fellipe RSVP" });
}

function getOrCreateSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      "Received At",
      "Submitted At (ISO)",
      "Name",
      "Attending",
      "Guests",
      "Language",
    ]);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

/**
 * Run this ONCE from the Apps Script editor after deploying.
 * Creates a time-based trigger that emails an Excel (.xlsx) export every 15 days.
 */
function setupTriggerOnce() {
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === "emailRsvpExcel") {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }
  ScriptApp.newTrigger("emailRsvpExcel").timeBased().everyDays(15).create();
  // Send an immediate test export so you know it works
  emailRsvpExcel();
}

function emailRsvpExcel() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = getOrCreateSheet_();
  var values = sheet.getDataRange().getValues();
  var csv = values
    .map(function (row) {
      return row
        .map(function (cell) {
          var s = String(cell == null ? "" : cell);
          if (/[",\n]/.test(s)) return '"' + s.replace(/"/g, '""') + '"';
          return s;
        })
        .join(",");
    })
    .join("\n");

  var blob = Utilities.newBlob(csv, "text/csv", "Yuki-Fellipe-RSVPs.csv");
  // SpreadsheetApp can also export native Excel:
  var xlsx = exportSheetAsXlsx_(ss.getId());

  MailApp.sendEmail({
    to: EMAIL_TO,
    subject: "Yuki & Fellipe — RSVP list (every 15 days)",
    body:
      "Olá Fellipe,\n\nSegue em anexo a lista atualizada de confirmações de presença (RSVP).\n\nYuki & Fellipe Wedding Website\n",
    attachments: [xlsx || blob],
  });
}

function exportSheetAsXlsx_(spreadsheetId) {
  try {
    var url =
      "https://docs.google.com/spreadsheets/d/" +
      spreadsheetId +
      "/export?format=xlsx";
    var token = ScriptApp.getOAuthToken();
    var response = UrlFetchApp.fetch(url, {
      headers: { Authorization: "Bearer " + token },
      muteHttpExceptions: true,
    });
    if (response.getResponseCode() !== 200) return null;
    return response.getBlob().setName("Yuki-Fellipe-RSVPs.xlsx");
  } catch (err) {
    return null;
  }
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}