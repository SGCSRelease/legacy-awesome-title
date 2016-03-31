<script>
function Draw() {
	$.ajax({
		url: "/api/externals/",
		success: function (data) {
			$('#external_list').empty();
			var table = "<table class='table'>";
			table += "<thead class='thead-inverse'><tr><th>Site Name</th>";
			table += "<th>Site Username</th><th></th></tr></thead>";

			$.each(data, function (index, entry) {
					table += '<tbody><tr>';
					table += '<td>' + data[index].sitename + '</td>';
					table += '<td>' + data[index].site_username + '</td>';
					table += '<th>' + '<button type="button" class="btn btn-info-outline btn-sm" onClick="Change(' + data[index].idx + ')">' + "수정" + '</button>';
					table += ' <button type="button" class="btn btn-danger btn-sm" onClick="Del(' + data[index].idx + ')">' + "삭제" + '</button></th>';
					table += '</tr></tbody>';
			});

			table += '</table>';
			$('#external_list').append(table);
		},
		dataType: "json",
	});
}

function Del(idx) {
	if (confirm("삭제하시겠습니까?")) {
	$.ajax({
		url: "/api/externals/" + idx + "/",
		type: "DELETE"
	});

	alert("삭제 되었습니다.");
	}
	Draw();
}

function Change(idx) {
	$.ajax({
		url: "/api/externals/" + idx + "/",
		type: "PUT"
	});
	Draw();
}

function Register(){
	$.ajax({
		url: "/api/externals/",
		type: "POST"
	});
}
	Draw();
</script>
