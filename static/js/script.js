// API URL

const API_URL = "/api/students";




// =============================
// LOAD STUDENTS WHEN PAGE OPENS
// =============================


document.addEventListener(

    "DOMContentLoaded",

    function () {

        loadStudents();

    }

);





// =============================
// GET ALL STUDENTS
// =============================



function loadStudents() {


    fetch(API_URL)


        .then(

            response => response.json()

        )


        .then(

            students => {


                let table = document.getElementById(
                    "studentTable"
                );



                table.innerHTML = "";




                students.forEach(

                    student => {


                        table.innerHTML += `


<tr>

<td>${student.id}</td>

<td>${student.name}</td>

<td>${student.age}</td>

<td>${student.course}</td>

<td>${student.city}</td>


<td>


<button onclick="editStudent(
${student.id},
'${student.name}',
${student.age},
'${student.course}',
'${student.city}'
)">

Edit

</button>



<button onclick="deleteStudent(${student.id})">

Delete

</button>


</td>


</tr>


`;

                    }

                );


            }

        );


}







// =============================
// ADD AND UPDATE STUDENT
// =============================



document.getElementById("studentForm")

    .addEventListener(

        "submit",

        function (event) {


            event.preventDefault();



            let id = document.getElementById("studentId").value;



            let student = {


                name: document.getElementById("name").value,


                age: document.getElementById("age").value,


                course: document.getElementById("course").value,


                city: document.getElementById("city").value


            };




            let method;

            let url;



            if (id) {


                method = "PUT";

                url = `${API_URL}/${id}`;


            }

            else {


                method = "POST";

                url = API_URL;


            }





            fetch(

                url,

                {

                    method: method,


                    headers: {

                        "Content-Type": "application/json"

                    },


                    body: JSON.stringify(student)

                }

            )


                .then(

                    response => response.json()

                )


                .then(

                    data => {


                        alert(data.message);



                        document.getElementById(
                            "studentForm"
                        ).reset();



                        document.getElementById(
                            "studentId"
                        ).value = "";



                        document.getElementById(
                            "submitBtn"
                        ).innerText = "Add Student";



                        loadStudents();


                    }

                );



        }

    );








// =============================
// EDIT STUDENT
// =============================



function editStudent(

    id,

    name,

    age,

    course,

    city

) {



    document.getElementById(
        "studentId"
    ).value = id;



    document.getElementById(
        "name"
    ).value = name;



    document.getElementById(
        "age"
    ).value = age;



    document.getElementById(
        "course"
    ).value = course;



    document.getElementById(
        "city"
    ).value = city;



    document.getElementById(
        "submitBtn"
    ).innerText = "Update Student";



}









// =============================
// DELETE STUDENT
// =============================



function deleteStudent(id) {



    if (

        confirm(
            "Are you sure you want to delete?"
        )

    ) {



        fetch(

            `${API_URL}/${id}`,

            {

                method: "DELETE"

            }

        )


            .then(

                response => response.json()

            )


            .then(

                data => {


                    alert(data.message);


                    loadStudents();


                }

            );



    }



}