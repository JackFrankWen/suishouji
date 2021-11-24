__utils = {
    formatDate: ( current_datetime ) => {
        let formatted_date
        if(current_datetime){
            if(current_datetime instanceof Date) {

                formatted_date = current_datetime.getFullYear()
                    + "-" + (current_datetime.getMonth() + 1)
                    + "-" + current_datetime.getDate()
                    + " " + current_datetime.getHours()
                    + ":" + current_datetime.getMinutes();
            }  else {
                const date = new Date(current_datetime)
                formatted_date = date.getFullYear()
                    + "-" + (date.getMonth() + 1)
                    + "-" + date.getDate()
                    + " " + date.getHours()
                    + ":" + date.getMinutes();
            }
            return formatted_date;
        }
        return ''
    },
     numFormat:(val)=>{
          if (!val) return 0.0
          let USPrice = Number.parseFloat(val).toLocaleString('en-US')

          let lastDot = USPrice.toString().indexOf('.')
          // 完全是整數, 需要新增小數點
          if (lastDot === -1) USPrice += '.00'

          // 返回資料是一位小數，用0補齊為兩位小數
          if (USPrice.toString().substring(lastDot + 1).length === 1) USPrice += '0'

          return '￥' + USPrice
        }
}