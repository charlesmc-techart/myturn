/**
 * @fileoverview Script for forcibly refreshing =IMPORTDATA() every hour even
 * when the spreadsheet isn't active
 */

const SPREADSHEET_ID = "";
const CELL = "";
const DATA_URL = "";

/**
 * @param {string} spreadsheetId ID of the spreadsheet file
 * @param {string} sheetCell Name + cell where =IMPORTDATA() is written
 * @param {string} sourceUrl URL of the data source
 * @return {Spreadsheet} The spreadsheet file
 */
function setById(spreadsheetId, sheetCell, sourceUrl) {
  const spreadsheet = SpreadsheetApp.openById(spreadsheetId);

  spreadsheet.getRange(sheetCell).setValue(`=IMPORTDATA("${sourceUrl}")`);

  return spreadsheet;
}

function refreshImportdata() {
  setById(SPREADSHEET_ID, CELL, DATA_URL);
}

function buildTrigger() {
  ScriptApp.newTrigger("refreshImportdata").timeBased().everyHours(1).create();
}
