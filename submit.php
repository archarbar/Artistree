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
?>

<html>
<head> 

	<meta name="viewport" content="width=device-width, initial-scale=1.0"> 
	<title>Results <?php ?></title>
	<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"> 
	<link rel="stylesheet" type="text/css" href="style.css"> 
	<link rel="shortcut icon" href="img/favicon.png">
	<link rel="stylesheet" type="text/css" href="style.css">
	<script src="https://d3js.org/d3.v6.min.js"></script>
</head>
<body class="result">
<a style="font-size:13px;font-family:Courier;margin-right:5px;margin-top:0px;position:absolute;color:white;right:0;" href="about.html">About Artistree</a>
<a style="font-size:14px;font-family:Courier;margin-left:5px;margin-top:0px;position:absolute;color:white;" href="index.html">Artistree</a>
<h4 align="center"> Artist:<?php echo " ".$artist;?></h4>
<?php
$output = shell_exec("python ./src/genius.py $artist 2>&1"); //change this to python3 when uploading to server
?>

<center>
<svg></svg>
</center>
<script>
raw=(<?php echo '`'.$output.'`' ?>).toString().replace(/\n/g," ");
raw=raw.replace(/'/g, '"');
console.log(raw);
dataRaw=JSON.parse(raw) ;

for (x in dataRaw) {
	if(dataRaw[x][0]==0){
		var parsed={name:x, count:dataRaw[x][0], url:dataRaw[x][1], children:[]};
	}
}
for (x in dataRaw) {
	if(dataRaw[x][0]!=0){
		var subParsed={name:x, count:dataRaw[x][0], url:dataRaw[x][1], children:[]};
		parsed.children.push(subParsed);
	}
}



const svg = d3.select('svg');
const width= document.body.clientWidth;
const height =  document.body.clientHeight;
const margin= { top:0, right:110, bottom:0, left:90};
const innerWidth = width - margin.left - margin.right;
const innerHeight = height - margin.top - margin.bottom;
const treeLayout= d3.tree().size([innerHeight, innerWidth]);

	
const g = svg 
	.attr('width', width)
	.attr('height', height)
	.append('g')
		.attr('transform', `translate(${margin.left},${margin.top})`);
			 
  
//promise for loading the json file. Only now for development. Then the json will be send through python

data=parsed;
const root = d3.hierarchy(data);
const links = treeLayout(root).links();
const linkPathGenerator = d3.linkHorizontal()
	.x(d => d.y)
	.y(d => d.x);

g.selectAll('path').data(links)
	.enter().append('path')
		.attr('d', linkPathGenerator);
		
		
g.selectAll('text').data(root.descendants())
	.enter().append('text')
		.attr('y', d => d.x)
		.attr('x', d => d.y)
		.attr('dy', '0.32em')
		.attr('font-size', d => 2/((d.depth+1))+0.2+'em')
		.attr('text-anchor', 'middle')
		.text(d=> d.depth ? d.data.name+": "+d.data.count : d.data.name);	


g.selectAll('image').data(root.descendants())
	.enter().append('image')
		.attr('xlink:href', d => d.data.url)
		.attr('y', d => d.x+15/((d.depth+1)))
		.attr('x', d => d.y)
		.attr("width", d => 150/((d.depth+1))+"px")
		.attr("height", "70px");
		

//window.scrollTo(0,document.body.scrollHeight);


</script>
<script>

</script>

</body>
</html>

