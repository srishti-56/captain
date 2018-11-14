var obj={
    xhr:new XMLHttpRequest(),
    get:function(event){
        var div = document.getElementById('data')
        div.innerHTML = "Hi"
        this.xhr.onreadystatechange=this.update;
        this.xhr.open("GET",url,true);
        this.xhr.send();
    },
    update:function(){
        if(this.readyState==4 && this.status==200){
            var res=this.responseText;
            /*The JSON.parse() method parses a JSON string, constructing the JavaScript value or object described by the string. */
            var resJSON=JSON.parse(res);
            var div = document.getElementById('data')
            for (var key in p) {
                if (p.hasOwnProperty(key)) {
                    div.innerHTML += (key+' '+p[key]);
                }
            }
           
        
        }
    }


}