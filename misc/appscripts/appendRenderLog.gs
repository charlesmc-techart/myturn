/**
 * @fileoverview Script for appending rendering data from a TSV file to the
 * spreadsheet
 */

const TSV_ID = "";
const SPREADSHEET_ID = "";
const SHEET_NAME = "";

/**
 * @param {string} tsvId
 * @return {!Array<!Array<string>>}
 */
function parseTsv(tsvId) {
  const data = DriveApp.getFileById(tsvId).getBlob().getDataAsString();
  return Utilities.parseCsv(data, "\t");
}

/**
 * @param {Sheet} sheet
 * @param {!Array<!Array<string>>} data
 */
function appendToSheet(sheet, data) {
  const rowToAppendTo = sheet.getLastRow() + 1;

  const numRows = data.length;
  const numColumns = data[0].length;

  sheet.getRange(rowToAppendTo, 1, numRows, numColumns).setValues(data);
}

/**
 * @param {Sheet} sheet
 * @return {boolean} True if the sheet is empty
 */
function sheetIsEmpty(sheet) {
  const range = sheet.getDataRange().getValues();
  const numRows = range.length;
  const numColumns = range[0].length;
  const cellContent = range[0][0];
  return numRows == 1 && numColumns == 1 && cellContent === "";
}

/**
 * Filter out data already on the sheet
 * @param {Sheet} sheet
 * @param {!Array<!Array<string>>} data
 * @param {number} columnToCheck
 * @return Only new data
 */
function filterData(sheet, data) {
  const columnToCheck = data[0].length;

  const lastRow = sheet.getLastRow() - 1;
  const sheetData = sheet.getRange(2, columnToCheck, lastRow).getValues();

  let rowNum;
  if (sheetData[0][0] === "Date") {
    rowNum = 0;
  } else {
    rowNum = 1;
  }
  for (; rowNum < data.length; ++rowNum) {
    let value = data[rowNum][columnToCheck - 1];
    if (!sheetData.some((contents) => contents.includes(value))) {
      break;
    }
  }
  return data.slice(++rowNum);
}

/**
 * @param {Sheet} sheet
 * @param {number} columnNum
 */
function deleteDuplicateRows(sheet, columnNum) {
  const lastRow = sheet.getLastRow();
  const data = sheet.getRange(`1:${lastRow}`);
  data.removeDuplicates([columnNum]);
}

function appendRenderLog() {
  const sourceData = parseTsv(TSV_ID);
  const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
  let sheet = spreadsheet.getSheetByName(SHEET_NAME);
  if (sheet === null) {
    sheet = spreadsheet.insertSheet(SHEET_NAME);
    appendToSheet(sheet, sourceData);
  } else if (sheetIsEmpty(sheet)) {
    appendToSheet(sheet, sourceData);
  } else {
    const filteredData = filterData(sheet, sourceData);
    if (filteredData.length > 0) {
      appendToSheet(sheet, filteredData);
    } else {
      console.log("Nothing to append");
    }
  }
}

function buildTrigger() {
  ScriptApp.newTrigger("appendRenderLog").timeBased().everyHours(1).create();
}
