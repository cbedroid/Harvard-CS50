var to = null;
var count = 0;
function changingText(secs){
  var id = $("#changing-text");
  var text = ["The best website ever","Wow, this is amazing!",
              "5 stars :-)", "Highest quality of books ever",
              "Happy happy","I found my favorite books!"];
  var length = text.length;
   
  if (count >= length){
    count=0;
  };

    $(id).html(text[count]);
    count+=1;
    console.log("TEXT:",text[count],"\nCount:",count);
    to = setTimeout(changingText,3000);
  }

///changingText();
$("#form-sorter").change(function(){
  console.log('Script Running'); 
  var sort = $("#sortby")[0];
  var order = $("#orderby")[0];
  var sortform = $("#form-sorter");
  if (sort.value != 'none' && order.value != 'none'){
    console.log('SORT:',sort.value,"\nORDER:",order.value)
    $(sortform).submit()
  return;
  };
 })
