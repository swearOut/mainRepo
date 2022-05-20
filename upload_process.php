<!DOCTYPE html>
<html>
        <head>
        <link rel="stylesheet" type="text/css" href="css/main.css">
        </head>
        <body>
            <div class="main_wrapper">
  <img src="./bannerimage/twitter_header_photo_2.png" style="width: 100%; height: auto;" alt="logo">
  <div class="form_wrapper">
    <p class="title">필터링 결과</p>
<?php
$db_conn = mysqli_connect("211.108.154.160","ncoa", "ncoa!!thanks", "pbl19");

//파일의 유효성
if(isset($_FILES["upfile"]) && $_FILES["upfile"]["name"] != "") {
    $file = $_FILES["upfile"];
    $upload_directory = "./inputData/";

    $filename  = $_FILES['upfile']['name']; // 업로드 하려한 파일명
    $filepath = urlencode($filename); // 한글파일 명을 대비
    $dest_file = $upload_directory.$filepath; 
    if(move_uploaded_file($file["tmp_name"], $dest_file)) {
        $query = "INSERT INTO upload_video(file_id, name_orig, name_save, reg_time) VALUES(?,?,?,now())";
        $file_id = md5(uniqid(rand(), true));
        $name_orig = $file["name"];
        $name_save = $path;
        $stmt = mysqli_prepare($db_conn, $query);
        $bind = mysqli_stmt_bind_param($stmt, "sss", $file_id, $name_orig, $name_save);
        $exec = mysqli_stmt_execute($stmt);
        echo '<a class="common_btn" href="file_list.php"><p class="">업로드 파일 목록</p></a>';
    }
    // echo $dest_file; //./inputData/test3.mp4
    // echo $name_orig; //test3.mp4
    $uploadfiledirectory = "/var/www/html/webpage/inputData/";

    //파이썬
    $is_file_exist = file_exists($uploadfiledirectory.$filename);
    if ($is_file_exist) {
        $tmp1 = "cd /var/www/html/webpage/pythonDir/ && python3 usingClova.py ".$uploadfiledirectory.$name_orig." 2>&1"; //클로바 가동 python file 실행
        $tmp2 = "cd /var/www/html/webpage/pythonDir/ && python3 STTResultPrePro.py"." 2>&2"; //stt전처리
        $tmp3 = "cd /var/www/html/webpage/pythonDir/ && python3 load_CNN_model.py"." >out.txt"; //모델가동
        $tmp4 = "cd /var/www/html/webpage/pythonDir/ && python3 makeVideo.py ".$uploadfiledirectory.$name_orig." ".$name_orig." >hoxy.txt "; //비디오 재가공
        // $tmp4 = "cd /var/www/html/webpage/pythonDir/ && python3 makeVideo1.py ".$uploadfiledirectory.$name_orig." ".$name_orig." >hoxy.txt "; //비디오 재가공

        if (shell_exec($tmp1) == null) {
                echo("<h3>클로바 가동 실패</h3>");
        }else{
                echo "<p></p>";
                shell_exec("time.sleep(3)");
                if (shell_exec($tmp2) == null) {
                    echo("<h3>영상 전처리 실패</h3>");
                }else{ 
                        shell_exec("time.sleep(5)");
                        if (shell_exec($tmp3) == null) {
                            if (shell_exec($tmp4) == null) {
                                // echo("<h3>비디오 재가공 실패</h3>");
                                }else{
                                    echo "<p>성공!</p>";
                                }
                        }else{
                            
                        }
                    }
                    
            
        }
    }
    else {
      echo '<h3>파일이 유효하지 않습니다.</h3>';
    }
}
else {
    echo "<h3>파일 업로드 또는 필터링 과정 중 오류 발생하였습니다.</h3>";
    echo '<a class="common_btn" href="javascript:history.go(-1);"><p>이전 페이지</p></a>';
}
mysqli_close($db_conn);
?>
</div>
</div>
</body>
</html>