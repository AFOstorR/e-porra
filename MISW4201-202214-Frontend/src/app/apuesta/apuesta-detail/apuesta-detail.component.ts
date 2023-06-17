import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Apuesta } from '../apuesta';
import { ApuestaService } from '../apuesta.service';

@Component({
  selector: 'app-apuesta-detail',
  templateUrl: './apuesta-detail.component.html',
  styleUrls: ['./apuesta-detail.component.css']
})
export class ApuestaDetailComponent implements OnInit {

  @Input() carrera: string;
  @Input() competidor: string;
  @Input() inputApuesta: Apuesta;

  userId: number;
  token: string;
  esApostador: boolean;

  constructor(
    private apuestaService: ApuestaService,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService
  ) { }

  ngOnInit() {
    let tmpInofUsuario:any = localStorage.getItem('usuario')
    this.userId = parseInt(this.router.snapshot.params.userId)
    this.token = this.router.snapshot.params.userToken
    this.esApostador = JSON.parse(tmpInofUsuario).es_apostador
  }

  eliminarApuesta() {
    this.apuestaService.eliminarApuesta(this.inputApuesta.id || 0, this.token)
      .subscribe(respuesta => {
        this.showSuccess()
        window.location.reload()
      },
        error => {
          this.showError("Ha ocurrido un error. " + error.message)
        })
  }

  goToEdit() {
    this.routerPath.navigate([`/apuestas/editar/${this.inputApuesta.id}/${this.userId}/${this.token}`])
  }

  showError(error: string) {
    this.toastr.error(error, "Error de autenticación")
  }

  showWarning(warning: string) {
    this.toastr.warning(warning, "Error de autenticación")
  }

  showSuccess() {
    this.toastr.success(`La carrera fue eliminada`, "Eliminada exitosamente");
  }
}
