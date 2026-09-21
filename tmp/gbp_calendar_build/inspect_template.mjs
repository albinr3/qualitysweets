import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const sourcePath = "C:/Users/Albin Rodriguez/Downloads/Calendario_GBP_52_Semanas_Dukes_Steakhouse.xlsx";
const input = await FileBlob.load(sourcePath);
const workbook = await SpreadsheetFile.importXlsx(input);
const overview = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 12000,
  tableMaxRows: 12,
  tableMaxCols: 16,
  tableMaxCellChars: 120,
});
console.log(overview.ndjson);
const sheet = workbook.worksheets.getItemAt(0);
console.log(JSON.stringify(sheet.getRange("A1:J56").values, null, 2));
