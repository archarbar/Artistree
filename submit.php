<html>
<head> 
	<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
	<title>Results <?php ?></title>
	<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"> <!--Link to boostrap to make a professional submit page -->	
	<link rel="stylesheet" type="text/css" href="style.css"> 
	<link rel="shortcut icon" href="img/favicon.png">
</head>
<body class="result">
<?php
//Down below template if we need to connect to a database
/*
$conn = mysqli_connect("localhost", "root", "TtTdWJ0aD2us", "swag");

//if connection to server/database has error
if (!$conn){
        echo 'Connection error: ' . mysqli_connect_error();
}
$result = mysqli_query($conn, "SELECT * FROM swag");
if($result->num_rows != 0){
        while ($row = mysqli_fetch_assoc($result)){
                $data[] = $row;
        }
}

echo $data[0]["swag"];
echo $data[0]["count"];
*/

$artist= $_POST['artist'];
$output = shell_exec("python myscript.py $artist 2>&1"); //change this to python3 when uploading to server
echo "<h3>".$output."</h3>";
?>
<script src="https://d3js.org/d3.v6.min.js"></script> <!--Import d3.js -->
<script>
const svg = d3.select('svg');
const width=document.body.clientWidth;
const height = document.body.clientHeight;
//tree is a function from d3 that creates nodes and links
const treeLayout= d3.tree()
	.size([height, width]);
	
svg 
	.attr('width', width)
	.attr('height', height)
  
  
//promise for loading the json file. Only now for development. Then the json will be send through python
d3.json('artists.json')
	.then(data => {
		const root = hierarchy(data);
		treeLayout(root)
		console.log(data);
	});
	
	

</script>

</body>
</html>

