// import dayjs from 'dayjs'

// const tableheaders = [
//   { text: '居住地', value: '居住地' },
//   { text: '感染者数', value: '感染者' },
//   { text: '退院数', value: '退院' },
//   { text: '治療者数', value: '治療中' }
// ]
// type DataType = {
//   居住地: string | null
//   感染者数: string | null
//   退院数: string | null
//   治療者数: string | null
//   [key: string]: any
// }

// type TableDataType = {
//   居住地: DataType['居住地']
//   感染者数: DataType['感染者数']
//   退院数: DataType['退院数']
//   治療者数: DataType['治療者数']
// }

// type TableDateType = {
//   headers: typeof tableheaders
//   datasets: TableDataType[]
// }

// /**
//  * Format for DataTable component
//  *
//  * @param data - Raw data
//  */
// export default (data: DataType[]) => {
//   const tableDate: TableDateType = {
//     tableheaders,
//     datasets: []
//   }
//   data.forEach(d => {
//     const TableRow: TableDataType = {
//       居住地: d['居住地'] ?? '不明',
//       感染者数: d['感染者数'] ?? '不明',
//       退院数: d['退院数'] ?? '不明',
//       治療者数: d['治療者数'] ?? '不明'
//     }
//     tableDate.datasets.push(TableRow)
//   })
//   tableDate.datasets.sort((a, b) => (a === b ? 0 : a < b ? 1 : -1))
//   return tableDate
// }
