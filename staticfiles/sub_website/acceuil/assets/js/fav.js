let host = window.location.origin;
let fav_page = new URL('/add_fav',host)

function fetching(body)
{
    fetch(fav_page,{
      method:'POST',
      headers:{
          'Content-Type':'application/json', 
          'X-CSRFToken':'{{csrf_token}}',
          'X-Requested-With':'XMLHttpRequest'
              },

      body:JSON.stringify(body),
      mode:'cors',
      cache:'default',
      credentials:'include'      
  })
    .then((response)=>{

      let popup = new Notyf()
      if (body['action'] == 'add')
      {
        popup.confirm('Produit ajouté à vos favoris !')       
      }
      else
      {
      popup.confirm('Produit retiré de vos favoris !')
      }
    })
};

function fav_aliment(element, codebar, email)
{
    let body = {codebar : codebar, email : email};

    if (element.checked)
    {
        body["action"] = 'add';
      }
    else
    {
        body["action"] ='delete';
        console.log(body);
    }
    fetching(body)
}



function remove_fav(element,codebar, email)
{
  let body = {codebar : codebar, email : email, action:'delete'};
  let parent = element.parentNode;
  let grandparent = parent.parentNode;
  
  fetching(body);
  grandparent.removeChild(parent);

}