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
    }
}