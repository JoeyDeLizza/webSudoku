var express = require('express');
var app = express();
var bodyParser = require('body-parser');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true}));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.use(express.static(__dirname + '/assets'));
// Routes
app.get("/", async (req, res) => {
    res.render('index');

});

app.post("/solve", async (req, res) => {
    console.log(req.body);
    var gameData = getData(req.body);
    console.log(gameData);
    // call python sudoku solver
    const spawn = require("child_process").spawn;
    const pythonProcess = spawn('python',["./SudokuSolver.py", gameData]);
    
    pythonProcess.stdout.on('data', async (data) => {
	console.log(data.toString());
	let sol = data.toString().split("");
	console.log(sol)
	var solved
	// check if solution is valid
	if(sol[0] == '0') {
	    solved = "No Solution";
	} else {
	    solved = "Solved"
	}
	res.render('solution', {sol, solved});
	
    });


});

// Listen
app.listen(3000, () => {
    console.log('Server listing on 3000');
})

function getData(obj) {
    let keys = Object.keys(obj);
    var str = '';
    keys.forEach((key) => {
	str = str + obj[key];
    });
    return str;
    
}
