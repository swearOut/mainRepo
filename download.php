<?php

$file_id = $_REQUEST['file_id'];

$db_conn = mysqli_connect("","ncoa", "", "");

$query = "SELECT file_id, name_orig, name_save FROM upload_video WHERE file_id = ?";

$stmt = mysqli_prepare($db_conn, $query);


$bind = mysqli_stmt_bind_param($stmt, "s", $file_id);

$exec = mysqli_stmt_execute($stmt);


$result = mysqli_stmt_get_result($stmt);

$row = mysqli_fetch_assoc($result);


$name_orig = $row['name_orig']; //test3.mp4

$fileDir = "/var/www/html/webpage/outputData/";

$fullPath = $fileDir."result_". $name_orig;

$length = filesize($fullPath);

header("Content-Type: application/octet-stream");

header("Content-Length: $length");

header("Content-Disposition: attachment; filename=".iconv('utf-8','euc-kr',$name_orig));

header("Content-Transfer-Encoding: binary");

$fh = fopen($fullPath, "r");

fpassthru($fh);

mysqli_free_result($result);

mysqli_stmt_close($stmt);

mysqli_close($db_conn);

exit;

?>
