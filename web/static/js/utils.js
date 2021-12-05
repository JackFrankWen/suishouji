__utils = {
    formatDate: ( current_datetime ) => {
        if(current_datetime){
            if (typeof current_datetime === 'string'){
                const  re = current_datetime.replace('GMT','')
                return dayjs(re).format("YYYY-MM-DD HH:mm")
            }
            return dayjs(current_datetime).format("YYYY-MM-DD HH:mm")
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