import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Evento, Competidor } from 'src/app/carrera/carrera';
import { CarreraService } from 'src/app/carrera/carrera.service';
import { Usuario } from 'src/app/usuario/usuario';
import { UsuarioService } from 'src/app/usuario/usuario.service';
import { Apuesta } from '../apuesta';
import { ApuestaService } from '../apuesta.service';
import { TransaccionService } from 'src/app/transaccion/transaccion.service';

@Component({
  selector: 'app-apuesta-create',
  templateUrl: './apuesta-create.component.html',
  styleUrls: ['./apuesta-create.component.css']
})
export class ApuestaCreateComponent implements OnInit {

  userId: number
  token: string
  apuestaForm: FormGroup
  carreras: Array<Evento>
  competidores: Array<Competidor>
  esApostador: Boolean
  usuario: Usuario;
  apostadores: Array<Usuario>;
  eventoSeleccionado: any;
  apostadorSeleccionado: Usuario;

  constructor(
    private apuestaService: ApuestaService,
    private carreraService: CarreraService,
    private usuarioService: UsuarioService,
    private transaccionService: TransaccionService,
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService
  ) { }

  ngOnInit() {
    if (!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " ") {
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else {
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.usuario = JSON.parse(localStorage.getItem('usuario')!)
      this.token = this.router.snapshot.params.userToken
      this.apuestaForm = this.formBuilder.group({
        id_evento: ["", [Validators.required]],
        id_competidor: ["", [Validators.required]],
        nombre_apostador: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(128)]],
        valor_apostado: ["5000", [Validators.required, Validators.min(5000)]],
      })

      this.getCarreras();
      this.getApostadores();
    }
  }

  onCarreraSelect(event: any): void {

    if (event != null && event != "") {
      this.eventoSeleccionado = this.carreras.filter(x => x.id == event)[0]
      this.competidores = this.eventoSeleccionado.competidores;
    } else {
      this.competidores = [];
      this.eventoSeleccionado = {};
    }

  }

  getCarreras(): void {
    this.carreraService.getAllCarreras(this.token)
      .subscribe(carreras => {
        this.carreras = carreras
      },
        error => {
          console.log(error)
          if (error.statusText === "UNAUTHORIZED") {
            this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.")
          }
          else if (error.statusText === "UNPROCESSABLE ENTITY") {
            this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
          }
          else {
            this.showError("Ha ocurrido un error. " + error.message)
          }
        })

  }

  createApuesta(newApuesta: Apuesta) {
    let valor = newApuesta.valor_apostado?.toString() || '';
    let valorApuesta = parseInt(valor);

    this.userId = parseInt(this.router.snapshot.params.userId)
    this.apostadorSeleccionado = this.apostadores.find(ap => ap.nombre == newApuesta.nombre_apostador)!;

    if (this.usuario.es_apostador) {
      this.userId = Number(this.apostadorSeleccionado?.id)
      if (valorApuesta > this.usuario.monedero!) {
        this.showWarningSaldo(`No tiene fondos suficientes para realizar la apuesta. Saldo actual: $ ${this.usuario.monedero}`);
        return;
      }
    } else {

      if (this.apostadorSeleccionado.monedero! < valorApuesta) {
        this.showWarningSaldo(`El apostador ${this.apostadorSeleccionado.nombre} no tiene fondos suficientes para realizar la apuesta. Saldo actual: $ ${this.apostadorSeleccionado.monedero}`);
        return
      }
    }

    this.apuestaService.crearApuesta(newApuesta, this.userId, this.token)
      .subscribe(usuario => {
        this.showSuccess(usuario)
        localStorage.setItem('usuario', JSON.stringify(usuario));
        this.apuestaForm.reset()
        this.routerPath.navigate([`/apuestas/${this.userId}/${this.token}`])
      },
        error => {
          if (error.statusText === "UNAUTHORIZED") {
            this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.")
          }
          else if (error.statusText === "UNPROCESSABLE ENTITY") {
            this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
          }
          else {
            this.showError("Ha ocurrido un error. " + error.message)
          }
          return
        })

    // if (this.usuario.es_apostador) {

    //   this.transaccionService.postTransaccion(this.usuario.id!, this.token, valorApuesta, 'apuesta').subscribe(r => {
    //     localStorage.setItem('usuario', JSON.stringify(r.usuario));
    //   })
    // } else {

    //   this.transaccionService.postTransaccion(apostadorSeleccionado!.id!, this.token, valorApuesta, 'apuesta').subscribe(r => {
    //   })
    // }

  }

  getApostadores() {
    this.usuarioService.getApostadores(this.token).subscribe(apostadores => {
      this.apostadores = apostadores;
    });
  }

  cancelCreate() {
    this.apuestaForm.reset()
    this.routerPath.navigate([`/apuestas/${this.userId}/${this.token}`])
  }

  showError(error: string) {
    this.toastr.error(error, "Error")
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación")
  }

  showSuccess(apuesta: Apuesta) {
    this.toastr.success(`La apuesta fue creada`, "Creación exitosa");
  }

  showWarningSaldo(message: string) {
    this.toastr.warning(message, "Monedero");
  }


}
