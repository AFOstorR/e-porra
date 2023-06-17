const { faker } = require('@faker-js/faker');

//un usuario administrador
// un apostador con 100.000 en el mondero
// minimo 2 carreras
// minimo 2 competidores por carrera

const usuario_test = {
    nombre: faker.name.fullName(),
    email: faker.internet.email().toLowerCase(),
    tarjetaCredito: faker.finance.account(16),
    password: faker.internet.password()
}

describe('Testing Apostador E-porra', () => {

    beforeEach(() => {
        cy.visit('https://e-porra-grupo11-angular.herokuapp.com/')
        cy.wait(500)
    })

    // Escenario #1 registrar usuario e inciciar sesión
    it('Registrarse e iniciar sesión', () => {
        cy.get('#lnRegristrate').click() //Botón registrarse

        //Formulario registro
        cy.get('form').within(() => {
            cy.get('#nombre').type(usuario_test.nombre)
            cy.get('#usuario').type(usuario_test.email)
            cy.get('#tarjetaCredito').type(usuario_test.tarjetaCredito)
            cy.get('#password').type(usuario_test.password)
            cy.get('#confirmPassword').type(usuario_test.password)
            cy.get('#registrarse').click() //Submit
        })
        cy.wait(500)
        //Nombre de usuario en el navbar
        cy.get('form').within(() => {
            cy.get('label').contains(usuario_test.nombre);
        });
        // Mensaje de alerta exitoso
        cy.get('div[role=alert]').contains(`Se ha registrado exitosamente`);
        cy.get('#btnSalir').click()

        cy.wait(500)
        //Iniciar sesión
        cy.get('#usuario').type(usuario_test.email)
        cy.get('#contrasena').type(usuario_test.password)
        cy.get('#btnIngresar').click()//submit login
        //Nombre de usuario en el navbar
        cy.get('form').within(() => {
            cy.get('label').contains(usuario_test.nombre);
        });

        cy.wait(500)
        cy.get('#btnSalir').click()
    });
    
    //Escenario #2: Iniciar sesión y ver opciones del menú apostador
    it('Iniciar sesión y ver opciones del menú apostador', () => {
        //form
        cy.get('#usuario').type(usuario_test.email)
        cy.get('#contrasena').type(usuario_test.password)
        cy.get('#btnIngresar').click()//submit login

        cy.wait(500)

        //Navbar 
        cy.get('#navbarSupportedContent').within(() => {
            //Logo/nombre App
            cy.get('#homeEporra').contains('E-Porra');

            //Nombre de usuario
            cy.get('form').within(() => {
                cy.get('label').contains(usuario_test.nombre);
            })

            //Opciones del menú
            cy.get('li.nav-item').within(() => {
                cy.get('#lnCarreras').filter(':contains("Carreras")');
                cy.wait(250)
                //Opción monedero - cargar cuenta 
               cy.get('a.nav-link').filter(':contains("Monedero")').click();
               cy.wait(200)
               cy.get('#lnCargar').filter(':contains("Cargar cuenta")').click();
               cy.wait(200)

            });
        });

        //Opción monedero - retirar dinero
        cy.get('#navbarSupportedContent').within(() => {
            cy.get('li.nav-item').within(() =>{
                cy.get('a.nav-link').filter(':contains("Monedero")').click();
                cy.wait(200)
                cy.get('#lnRetirar').filter(':contains("Retirar dinero")').click();
                cy.wait(500)

            })
        })

        //Opción Apuestas
        cy.get('#navbarSupportedContent').within(() => {
            cy.get('li.nav-item').within(() =>{
                cy.get('a.nav-link').filter(':contains("Apuestas")').click();
                cy.wait(500)
                
            })
        })

    })
    
    
    //Escenario #3: Iniciar sesión y cargar dinero en la cuenta
    it('Iniciar sesión y cargar dinero en la cuenta', () => {
        //form
        cy.get('#usuario').type(usuario_test.email)
        cy.get('#contrasena').type(usuario_test.password)
        cy.get('#btnIngresar').click()//submit login

        cy.wait(500)

        //Navbar 
        cy.get('#navbarSupportedContent').within(() => {

            //Opciones del menú
            cy.get('li.nav-item').within(() => {

                cy.get('a.nav-link').filter(':contains("Monedero")').click();

                cy.wait(200)
                cy.get('a.dropdown-item').filter(':contains("Cargar cuenta")').click();
                cy.wait(500)
            });
        });

        cy.get('form').within(() => {
            cy.get('#valor').type(faker.datatype.number({ min: 150000 }));
            cy.get('#btnDepositar').click()//submit login
        });

        // Mensaje de alerta exitoso
        cy.get('div[role=alert]').contains(`El dinero fue depositado a la cuenta`);


    });

    //Escenario #4: Iniciar sesión y retirar dinero en la cuenta
    it('Iniciar sesión y retirar dinero en la cuenta', () => {
        //form
        cy.get('#usuario').type(usuario_test.email)
        cy.get('#contrasena').type(usuario_test.password)
        cy.get('#btnIngresar').click()//submit login

        cy.wait(500)

        //Navbar 
        cy.get('#navbarSupportedContent').within(() => {

            //Opciones del menú
            cy.get('li.nav-item').within(() => {

                cy.get('a.nav-link').filter(':contains("Monedero")').click();

                cy.wait(200)
                cy.get('a.dropdown-item').filter(':contains("Retirar dinero")').click();
                cy.wait(500)
            });
        });

        /*cy.get('#txtSaldo').invoke('text').then((text) =>{
            saldo = text.slice(2)
        })*/
        
        cy.get('form').within(() => {
            cy.get('#valor').type(faker.datatype.number({max:10000}));
            cy.get('#btnRetirar').click({force: true})//submit login
        });
        cy.wait(250)
        // Mensaje de alerta exitoso
        cy.get('div[role=alert]').contains(`El dinero fue retirado de la cuenta`);


    });
    
    //Escenario #5: Iniciar sesión y realizar apuestas y seleccionarlas del listado para ver el detalle
    it('Iniciar sesión y realizar apuestas y ver listdo', () => {
        cy.get('#usuario').type(usuario_test.email)
        cy.get('#contrasena').type(usuario_test.password)
        cy.get('#btnIngresar').click()//submit login

        cy.wait(500)

        //Navbar 
        cy.get('#navbarSupportedContent').within(() => {

            //Opciones del menú
            cy.get('li.nav-item').within(() => {
                cy.get('a.nav-link').filter(':contains("Apuestas")').click();
                
            });
        });

        cy.get('#btnCrearApuesta').click();

        //Formulario crear apuesta
        cy.get('form').within(() => {
            cy.get('#carrera').select(1);
            cy.get('#competidor').select(1);
            
            cy.get('#valor').clear().type(faker.datatype.number({ min: 5000, max:20000 }));
            cy.get('#btnCrear').click({force: true})//submit crear apuesta
        });

        //Alerta confirmación
        cy.get('div[role=alert]').contains(`La apuesta fue creada`);
        cy.wait(1000)

        cy.get('#btnCrearApuesta').click();
        cy.wait(1000)
        //Formulario crear apuesta
        cy.get('form').within(() => {
            cy.get('#carrera').select(2);
            cy.get('#competidor').select(2);
            
            cy.get('#valor').clear().type(faker.datatype.number({ min: 5000, max:10000 }));
            cy.get('#btnCrear').click({force: true})//submit crear apuesta
        });

        //Alerta confirmación
        cy.get('div[role=alert]').contains(`La apuesta fue creada`);
        cy.wait(1000)

        cy.get('#tlApuestas').within(()=>{
            cy.get('tr').last().click()
            cy.wait(1000)
            cy.get('tr').first().click()
        });
    });
    
    
    //Escenario #6: Iniciar sesión y actualizar perfil
    it('Iniciar sesión y Actualizar perfil', () => {
        cy.get('#usuario').type(usuario_test.email)
        cy.get('#contrasena').type(usuario_test.password)
        cy.get('#btnIngresar').click()//submit login

        cy.wait(500)

        //Navbar 
        cy.get('#navbarSupportedContent').within(() => {
            //Opciones del menú
            cy.get('li.nav-item').within(() => {
                cy.get('a.nav-link').filter(':contains("Perfil")').click();
                
            });
        });

        let nuevo_correo = faker.internet.email().toLowerCase();
        let nuev_tarjeta = faker.finance.account(16);
        cy.get('form').within(() => {
            cy.get('#btnCorreoElectronico').clear().type(nuevo_correo);
            cy.get('#btnNumeroTarjeta').clear().type(nuev_tarjeta);
            
            cy.get('#btnActualizar').click({force: true})//submit crear apuesta
        });

        //Alerta confirmación
        cy.get('div[role=alert]').contains(`La información de usuario fue actualizada`);
        cy.wait(500)

        //Navbar 
        cy.get('#navbarSupportedContent').within(() => {
            //Opciones del menú
            cy.get('li.nav-item').within(() => {
                cy.get('a.nav-link').filter(':contains("Perfil")').click();
                
            });
        });

    });
    
});



