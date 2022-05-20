<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css">
</head>
<body>
<div style="width:fit-content;" class="form_wrapper" >
<p class="title">File List</p>
<table style="">
<tr>

        <th bgcolor="#6495ED">파일 아이디</th>

        <th bgcolor="#6495ED">원래 파일명</th>

        <th bgcolor="#6495ED">저장된 파일명</th>

</tr>

<?php
//delete from upload_video;

$db_conn = mysqli_connect("211.108.154.160","ncoa", "ncoa!!thanks", "pbl19");

$query = "SELECT file_id, name_orig, name_save FROM upload_video ORDER BY reg_time DESC";

$stmt = mysqli_prepare($db_conn, $query);

$exec = mysqli_stmt_execute($stmt);

$result = mysqli_stmt_get_result($stmt);

while($row = mysqli_fetch_assoc($result)) {

?>

<tr>

  <td><?= $row['file_id'] ?></td>

  <td><a href="download.php?file_id=<?= $row['file_id'] ?>" target="_blank"><?= $row['name_orig'] ?></a></td>

  <td><?= $row['name_save'] ?></td>

</tr>

<?php
} 
mysqli_free_result($result);

mysqli_stmt_close($stmt);

mysqli_close($db_conn);

?>
</table>
</div>
</body>
</html>