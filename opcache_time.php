<?php

#var_dump($dir);
/*
function dir_calculate($root){
	$dir = scandir($root);
}
$global_compile_time = 0;
foreach($dir as $name){
	if(strpos(".php", strtolower($name)) >= 0){
		$t1 = time($get_as_float=true);
		opcache_compile_file($name);
		$t2 = time($get_as_float=true);
		$global_compile_time += ($t2 - $t1);
	}
}
*/

//foreach (glob("*/*/*/*/*/*/*/*/*/*/*/*/*/*/*.php") as $filename) {
//    echo "$filename";
//	echo "<br>";
//}

//phpinfo();

$global_compile_time = 0;
$pattern = "*.php";


while(true){
	
	$iter = glob($pattern);
	if(count($iter) <= 0){
		break;
	}
	//echo count($iter);
	//echo "<br>";
	foreach($iter as $filename){
		
		try{
			if($filename != "opcache_time.php"){
				//echo $filename."<br>";
				$t1 = microtime($get_as_float=true);
				opcache_compile_file($filename);
				
				$t2 = microtime($get_as_float=true);
				$global_compile_time += ($t2 - $t1);
			}
		}
		catch(Exception $e){
			print_r("EXCPP");
		}
	}
	
	$pattern = "*/".$pattern;
	
	//break;
}
echo $global_compile_time;


?>
