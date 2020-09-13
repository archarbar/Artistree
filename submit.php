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
	<title>Results For <?php echo " ".ucfirst($artist); ?></title>
	<link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"> 
	<link rel="stylesheet" type="text/css" href="style.css"> 
	<link rel="shortcut icon" href="img/favicon.png">
	<link rel="stylesheet" type="text/css" href="style.css">
	<script src="https://d3js.org/d3.v6.min.js"></script> <!--d3.js which is a very popular data visualisation library that works with javascript -->
</head>
<body class="result">
<a style="font-size:13px;font-family:Courier;margin-right:5px;margin-top:0px;position:absolute;color:white;right:0;" href="about.html">About Artistree</a>
<a style="font-size:14px;font-family:Courier;margin-left:10px;margin-top:0px;position:absolute;color:white;" href="index.html">Artistree</a>
<h2 align="center"> Artist:<?php echo " ".ucfirst($artist);?></h2>
<?php
$output = shell_exec("python ./src/genius.py $artist 2>&1"); //change this to python3 when uploading to server
?>

<center>
<svg></svg>
</center>
<script>
raw=(<?php echo '`'.$output.'`' ?>).toString().replace(/\n/g," "); //get data that was formatted by genius.py and replace newlines by spaces
raw=raw.replace(/'/g, '"'); //replace single quotes by double quotes
//console.log(raw); //debug
dataRaw=JSON.parse(raw) ; //transform the JSON string into a javascript object to manipulate and read it more easily

//create an second object 
//dataRaw -> parsed which will be the object used by d3.js, sinced the original python object is unusable.
//d3.js is very picky in how it handles objects

for (x in dataRaw) { //creating the main dictionnary with main artist
	if(dataRaw[x][0]==0){
		var parsed={name:x, count:dataRaw[x][0], url:dataRaw[x][1], children:[]}; 
	}
}
for (x in dataRaw) { //creating the children dictionaries of the linked artists
	if(dataRaw[x][0]!=0){
		var subParsed={name:x, count:dataRaw[x][0], url:dataRaw[x][1], children:[]};
		parsed.children.push(subParsed);
	}
}



const svg = d3.select('svg'); //getting svg element to change it using d3 functions
const width= document.body.clientWidth; //getting window width
var height =  document.body.clientHeight; //getting window height
const margin= { top:0, right:150, bottom:50, left:20};
const innerWidth = width - margin.left - margin.right;
if (height < ((parsed.children).length-1)*130) { //depending on how many artists were found, if this surpasses a limit, we need to make the scrollable window longer 
	height=((parsed.children).length-1)*130;
} 
const innerHeight= height - margin.bottom - margin.top; 
const treeLayout= d3.tree().size([innerHeight, innerWidth]);

	
const g = svg 
	.attr('width', width)
	.attr('height',height)
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
		.attr('text-anchor', d=> d.depth? 'end':'start')
		.text(d=> d.depth ? d.data.name+": "+d.data.count : d.data.name);	


g.selectAll('image').data(root.descendants())
	.enter().append('image')
		.attr('xlink:href', d => d.data.url)
		.attr('y', d => d.depth? d.x-36:d.x+20)
		.attr('x', d => d.depth? d.y+10:d.y)
		.attr("width", d => d.depth? "80px":"150px")
		.attr("height", d => d.depth? "80px":"150px");
		

//window.scrollTo(0,document.body.scrollHeight);


</script>
<script>

</script>

</body>
</html>

