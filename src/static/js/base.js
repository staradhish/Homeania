function level_add_function() {
	var pathname = window.location.pathname.split("/");
	var level = pathname[pathname.length-1];
	console.log(level)
	window.location = "/retake/" + level
	}



function get_answer() {
	//debugger;
   console.log("get_answer claase");
   var answer = $('input[name="marked_answer"]:checked').val();
   // var ques = $('span[name="marked_ques"]').val();
   var ques = $('#marked_ques').attr('value')
   var pathname = window.location.pathname.split("/");
   var level = pathname[pathname.length-1];
   // console.log("==== you select ===", answer)
   // console.log("==== you question ===", ques)
   // console.log("==== you question ===", level)

   $.ajax({
  type: "POST",
  url: '/test/',
  data: {csrfmiddlewaretoken: '{{csrf_token}}',
  	answer : answer, ques:ques, level:level
  },
   dataType : "json",
});
}
