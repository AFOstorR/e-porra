const { faker } = require('@faker-js/faker');

//un usuario administrador
// un apostador con 100.000 en el mondero
// minimo 2 carreras
// minimo 2 competidores por carrera

const usuarioAdmin = {
    email: 'administrador_eporr@uniandes.edu.co',
    password: 'adM1n4cc3S*'
}

describe('Testing Admin E-porra', () => {

    beforeEach(() => {
        cy.visit('https://e-porra-grupo11-angular.herokuapp.com/')
        cy.wait(500)
    })

    // Escenario #1 Iniciar sesión y verificar opciones de administrador
    /*  */
    it('Iniciar sesión y ver menú opciones Administrador', () => {

        cy.wait(250)
        //Iniciar sesión
        cy.get('#usuario').type(usuarioAdmin.email);
        cy.get('#contrasena').type(usuarioAdmin.password);
        cy.get('#btnIngresar').click();//submit login

        //Navbar 
        cy.get('#navbarSupportedContent').within(() => {
            //Logo/nombre App
            cy.get('#homeEporra').contains('E-Porra');

            //Nombre de usuario
            cy.get('form').within(() => {
                cy.get('label').contains('Administrador');
            })

            //Opciones del menú
            cy.get('li.nav-item').within(() => {
                cy.get('a.nav-link').filter(':contains("Carreras")').click();
                cy.wait(250)
                cy.get('a.nav-link').filter(':contains("Apuestas")').click();

            });
        });

    });

    //Escenario #2: Iniciar sesión y crear una carrera
    it('Iniciar sesión, crear una carrera, verla en el listado y seleccionarla', () => {
        //form login
        cy.get('#usuario').type(usuarioAdmin.email)
        cy.get('#contrasena').type(usuarioAdmin.password)
        cy.get('#btnIngresar').click()//submit login

        cy.wait(500)

        //Botón crear carrera
        cy.get('#btnIrCarrera').click()
        cy.wait(250)

        //Formulario carrera
        //Datos carrera
        let nombreCarrera = faker.name.fullName();
        cy.get('#nombreCarrera').type(nombreCarrera);
        //Competidor 1
        cy.get('#competidor-0').type(faker.name.fullName());
        cy.get('#probabilidad-0').type('0.5');

        cy.get('#btnAgregarCompetidor').click();
        //Competidor # 2
        cy.get('#competidor-1').type(faker.name.fullName());
        cy.get('#probabilidad-1').type('0.5');
        cy.get('#btnCrear').click();
        cy.wait(200);

        // Mensaje de alerta exitoso
        cy.get('div[role=alert]').contains(`La carrera ${nombreCarrera} fue creada`);

        //Busqueda 
        cy.get('input[type=search]').type(nombreCarrera);
        cy.wait(150);
        //Seleccion de la carrera para ver detalles
        cy.get('table').within(() => {
            cy.get('tr').filter(`:contains(${nombreCarrera})`).click()
        });

    })

    //Escenario #3: Iniciar sesión y crear una apuesta asociada a un apostador
    it('Iniciar sesión, crear una carrera, verla en el listado y seleccionarla', () => {
        //form login
        cy.get('#usuario').type(usuarioAdmin.email)
        cy.get('#contrasena').type(usuarioAdmin.password)
        cy.get('#btnIngresar').click()//submit login

        cy.wait(500)

        //Opción Apuestas
        cy.get('#navbarSupportedContent').within(() => {
            cy.get('li.nav-item').within(() =>{
                cy.get('a.nav-link').filter(':contains("Apuestas")').click();
                cy.wait(500)
            })
        })


        cy.get('#btnCrearApuesta').click();

        //Formulario crear apuesta
        cy.get('form').within(() => {
            cy.get('#carrera').select(1);
            cy.get('#competidor').select(1);
            cy.get('#apostador').select(1);
            
            cy.get('#valor').clear().type(faker.datatype.number({ min: 5000, max:6000 }));
            cy.get('#btnCrear').click({force: true})//submit crear apuesta
        });


    })

});



