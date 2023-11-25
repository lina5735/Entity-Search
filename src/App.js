import './App.css';
import React, {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {


  const [people, setPeople] = useState("")
  const [org, setOrg] = useState("")
  const [loc, setLoc] = useState("")
  const [date, setDate] = useState("")
  
  
  // const [result, setResult] = useState(`d75747a87ac6c574f7bb11080f38f1563ed14b46.story
  // d27044bfb4bc281dc8349aac09dad2e64be09411.story
  // ce8cf58260bbc82772d666ece733044297a1e680.story
  // c7fb0295ad6226798e65332c841f6a1508eb9efe.story
  // 73ce0c3dc5c0752bdb392ccae44bfb53cec60dfb.story
  // 7b9c0b64b7143a632af9455ce932c0a722b4e098.story
  // 72ba50a8077052f867a02c670d7f6ed874f4ba12.story
  // 057d4a3cf662f1bea473535288325bd481dd3b53.story
  // fbf5bd723e4c01a5fa2d0236d6eebe90f6527c2f.story
  // f29dd2478dd7000ecce5d27fb9225c798572aec3.story
  // e3522246231dcc0134cf1089ec77c7d0672c693f.story`)

  const [alert, setAlert] = useState("")
  const [runTime, setRunTime] = useState("")

  const [result, setResult] = useState("")
  

  const handleChange1 = (event) => {
    setPeople(event.target.value)
  }
  const handleChange2 = (event) => {
    setOrg(event.target.value)
  }
  const handleChange3 = (event) => {
    setLoc(event.target.value)
  }
  const handleChange4 = (event) => {
    setDate(event.target.value)
  }

  // useEffect (() => {
  //   fetch('/api/route').then(res => res.json()).then(
  //     data => {
  //       setResult(data.result)
  //     })
  // }, []);

  return (
    <div style={{maxWidth:1600}}>
				<h1 className="banner">
					Entity Search Demo 
				</h1>



        <div  className="content">

            <div className="search-entity"  > 
              <span  style={{width:120}}  className="input-group-text" >People</span>
              <input  style={{width:400}}   
                value={people} 
                onChange={handleChange1}
                type="text" className="form-control" />   
            </div>


            <div className="search-entity"  > 
              <span style={{width:120}}  className="input-group-text" >Location</span>
              <input  style={{width:400}}    
                value={loc} 
                onChange={handleChange3}
                 type="text" className="form-control" />   
            </div>

            <div className="search-entity"  > 
              <span style={{width:120}}  className="input-group-text" >Organization</span>
              <input  style={{width:400}}    
                value={org} 
                onChange={handleChange2}
                 type="text" className="form-control" />   
            </div>
            

            <div className="search-entity"  > 
              <span style={{width:120}}  className="input-group-text" >Date</span>
              <input  style={{width:400}}    
                value={date} 
                onChange={handleChange4}
                 type="text" className="form-control" />   
            </div>

            
                  
        </div>


        <div className='content'>  
              <button type="button" className="btn btn-outline-success" onClick={
                async () => {
                  const startTime = performance.now()
                  setRunTime("")
                  setAlert("Calculating Similarities...")
                  setResult("")
                  const query = {people, org, loc, date}
                  const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(query)
                  })

                  if (!response.ok){
                    setAlert("Query Failed!")
                  }

                  const data = await response.json();
                  const endTime = performance.now()
                  const fetchTime = endTime - startTime; 

                  setRunTime("Computation takes: "+(fetchTime / 60000).toFixed(2)+" minutes")
                  console.log(data.result)
                  setResult(data.result)
                  
                  // .then(res => res.json()).then(
                  //   data => {
                  //     setResult(data.result)
                  //     console.log(data.result)
                  //   }
                  // )
                  setAlert("Search done!")
                }
              }>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" className="bi bi-search" viewBox="0 0 16 16">
                  <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                </svg>
                Search
              </button> 
        </div>
        
       

        <div className='content'> 
          <div className='result'>
            {alert}
            <br></br>
            {runTime}
            <br></br>
            {result}
          </div>
          
        </div>

        

			</div>
  );
}

export default App;
