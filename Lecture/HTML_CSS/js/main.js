function headers(){
  $("#header").after(`
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="index.html"><img src="" alt=""></a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <a class="nav-item nav-link" href="courses.html">CS50<span class="sr-only">(current)</span></a>
            <a class="nav-item nav-link" href="home.html">HOME</a>
            <a class="nav-item nav-link" href="project.html">PROJECT</a>
          </div>
        </div>
      </nav>`);
};

$(document).ready(function() {
    $("[href]").each(function() {
        if (this.href == window.location.href) {
            $(this).addClass("active");
        }
    });
});

headers();

$('.carousel').carousel({
    interval: 2000
})


function java(){
  return `SQL (es-que-el) stands for Structured Query Language, is a programming language to operate databases. It includes storing, manipulating and retrieving data stored in a relational database. 
					SQL keeps data precise and secure, and it also helps in maintaining the integrity of databases, irrespective of its size.
					SQL is used today across web frameworks and database applications. If you are well versed in SQL, you can have better command over data exploration, and effective decision making.
					If you are planning to opt database management as your career, first go through C or C++. SQL developers are in great demand and offered high pay scales by reputed organizations.
				`;

}

