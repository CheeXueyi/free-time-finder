//fetch data from 
let dates = [1,2,3,4,5]
let range = {
    "start_time" : 0,
    "end_time" : 21
}

let not_free_times = [
    {
        "date":2,
        "start_time": 1,
        "end_time": 2,
        "free": false
    },
    {
        "date":3,
        "start_time": 3,
        "end_time": 4,
        "free": false
    }

]
for(let i = 0; i < dates.length; i++)
{
    let html = `
    <tr>
        <th>${dates[i]}</th>
    `
    for(let j = range["start_time"]; j <= range["end_time"]; j++)
    {
        html += "<td></td>"
    }
    
    document.getElementById("calendar").innerHTML += html;
}
