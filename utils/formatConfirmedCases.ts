type DataType = {
  attr: '検査実施人数'
  value: number
  children: [
    {
      attr: '感染者数'
      value: number
      children: [
        {
          attr: '治療中'
          value: number
        },
        {
          attr: '退院'
          value: number
        }
      ]
    }
  ]
}

type ConfirmedCasesType = {
  検査実施人数: number
  感染者数: number
  治療中: number
  退院: number
}

/**
 * Format for *Chart component
 *
 * @param data - Raw data
 */
export default (data: DataType) => {
  const formattedData: ConfirmedCasesType = {
    検査実施人数: data.value,
    感染者数: data.children[0].value,
    治療中: data.children[0].children[0].value,
    退院: data.children[0].children[1].value
  }
  return formattedData
}
