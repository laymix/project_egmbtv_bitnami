# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    ThinkOpen Solutions Brasil
#    Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
try:
     import cStringIO as StringIO
except ImportError:
     import StringIO
from openerp import models, api, fields,tools, _
from PIL import Image
from PIL import ImageEnhance
from random import randint
from openerp.exceptions import ValidationError

from datetime import datetime, time, date, timedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime


class task_type(models.Model):
    _name = 'task.type'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer('Color Index', size=1)
    task_id = fields.Many2one('project.task', string='Task')


class project_task(models.Model):
    _inherit = 'project.task'

    type_name = fields.Char(
        compute='_get_type_name',
        store=True,
        string='Name')
    task_type_id = fields.Many2one('task.type', string='Type')
    color = fields.Integer(compute='_get_color', string='Color', store=False)
    appro_marche=fields.Binary(string='Approbation de marché')
    num_marche=fields.Char(string='N° de marché')
    dep=fields.Char(string='Département')
    reg=fields.Char(string='Région')
    nomination=fields.Char(string='Nomination')
    odre_serv_up=fields.Binary(string='Documents à attacher')
    trav_dir=fields.Many2one('project.hr',string='Directeur des travaux')
    cond_trav=fields.Many2one('project.hr',string='Conducteur des travaux')
    resp_geo=fields.Many2one('project.hr',string='Responsable Géotechnique')
    resp_topo=fields.Many2one('project.hr',string='Responsable Topographie')
    comp_chantier=fields.Many2one('project.hr',string='Comptable de chantier')
    proj_exe_up=fields.Binary(string='Document à attacher')
    doc_geo_up=fields.Binary(string='Document à attacher')
    doc_topo_up=fields.Binary(string='Document à attacher')
    doc_approvis_up=fields.Binary(string='Document à attacher')
    doc_mat_dexe_up=fields.Binary(string='Document à attacher')
    doc_team_dexe_up=fields.Binary(string='Document à attacher')
    my_team_dexe_ids=fields.One2many('project.task.team.dexe','my_team_dexe_id',string='Equipe d\'exectution')
    planing_reunion_up=fields.Binary('Planning des réunions internes')
    my_inst_cht_ids=fields.One2many('project.task.inst.cht','my_inst_cht_id',string='Installation de chantier')
    my_task_trav_ids=fields.One2many('project.task.trav.prepa','my_task_trav_id',string='Travaux préparatoires')
    my_terr_gen_ids=fields.One2many('project.task.terr.gen','my_terr_gen_id',string='Terrassements Généraux')
    my_task_chauss_ids=fields.One2many('project.task.chauss','my_task_chauss_id',string='Chaussées')
    my_task_ass_ouv_prot_ids=fields.One2many('project.task.ass.ouv.prot','my_task_ass_ouv_prot_id',string='Assainissement Ouvrages et Protections')
    my_task_sec_sign_rout_ids=fields.One2many('project.task.sec.sign.rout','my_task_sec_sign_rout_id',string='Sécurité et Signalisations Routières')
    my_team_dexec_ids=fields.One2many('project.task.team.dexec','my_team_dexec_id',string='Equipe d\'exectution')
    estim_cout_pges=fields.Float('Estimation des coûts du PGES')
    estim_cout_pges_up=fields.Binary('Documents à attacher')
    my_fleet_cam_ids=fields.One2many('project.fleet.camion','my_fleet_cam_id',string='Camion')
    my_fleet_eng_ids=fields.One2many('project.fleet.engine','my_fleet_eng_id',string='Engin')
    my_matos_cmd_ids=fields.One2many('project.task.cmd.matos', 'my_matos_cmd_id',string='Materiaux')
    contrat_up=fields.Binary('Documents à attacher')

    @api.multi
    def name_get(self):
        result = []
        for task in self:
            task_type = task.task_type_id and task.task_type_id.name or ''
            result.append(
                (task.id, "%s %s" %
                 ('[' + (task_type)+ ']', task.name or ' ')))
        return result

    @api.depends('task_type_id.name')
    def _get_type_name(self):
        for record in self:
            if record.task_type_id:
                record.type_name = record.task_type_id.name

    @api.depends('task_type_id.color')
    def _get_color(self):
        for record in self:

            if record.task_type_id:
                record.color = record.task_type_id.color

    @api.onchange('task_type_id')
    def _change_task_type(self):
        if self.task_type_id:
            self.color = str(self.task_type_id.color)[-1]
            self.type_name = self.task_type_id.name
class project_task_team_dexe(models.Model):
     _name='project.task.team.dexe'

     name=fields.Char('Poste')
     emploi_assign=fields.Many2one('project.hr',string='Employé Assigné')
     date_assign=fields.Date('Date d\'assignement')
     date=fields.Date('Date')
     my_team_dexe_id=fields.Many2one('project.task',string='Equipe d\' éxécution')
     poste_id=fields.Many2one('project.hr.profession',string='Poste')
class project_task_team_dexec(models.Model):
     _name='project.task.team.dexec'

     name=fields.Char('Poste')
     emploi_assign=fields.Many2one('project.hr',string='Employé Assigné')
     date_assign=fields.Date('Date d\'assignement')
     date=fields.Date('Date')
     nombre=fields.Integer('Nombre')
     taux_horaires=fields.Integer(string='Taux Horaires')
     hr_trav=fields.Integer(string='Heures de travail')
     taux_sem=fields.Integer(string='Taux/Semaine')
     frais=fields.Float('Autres Frais')
     total=fields.Float('Total')
     my_team_dexec_id=fields.Many2one('project.task',string='Equipe d\' éxécution')
     poste_id=fields.Many2one('project.hr.profession',string='Poste')
class project_task_inst_cht(models.Model):
     _name='project.task.inst.cht'

     name=fields.Char('Désignation')
     my_cht_id=fields.Many2one('project.task.exe.design',string='Désignation')
     avancement=fields.Text('Avancement')
     date=fields.Date('Date')
     my_inst_cht_id=fields.Many2one('project.task',string='Installation de chantier')
class project_task_trav_prepa(models.Model):
    _name='project.task.trav.prepa'

    name=fields.Char('Désignation')
    my_trav_id=fields.Many2one('project.task.exe.design',string='Désignation')
    date=fields.Date('Date')
    caracteristique=fields.Text('Caractéristique')
    valeur=fields.Integer('Valeur')
    unite=fields.Char('Unité')
    valider=fields.Boolean('Valider')
    my_task_trav_id=fields.Many2one('project.task',string='Travaux préparatoires')
class project_task_ass_ouv_prot(models.Model):
    _name='project.task.ass.ouv.prot'

    name=fields.Char('Désignation')
    my_ouv_id=fields.Many2one('project.task.exe.design',string='Désignation')
    date=fields.Date('Date')
    caracteristique=fields.Text('Caractéristique')
    valeur=fields.Integer('Valeur')
    unite=fields.Char('Unité')
    valider=fields.Boolean('Valider')
    my_task_ass_ouv_prot_id=fields.Many2one('project.task',string='Assainissement Ouvrages et Protections')
class project_task_chauss(models.Model):
    _name='project.task.chauss'

    name=fields.Char('Désignation')
    my_chauss_id=fields.Many2one('project.task.exe.design',string='Désignation')
    date=fields.Date('Date')
    caracteristique=fields.Text('Caractéristique')
    valeur=fields.Integer('Valeur')
    unite=fields.Char('Unité')
    valider=fields.Boolean('Valider')
    my_task_chauss_id=fields.Many2one('project.task',string='Chaussées')
class project_task_sec_sign_rout(models.Model):
    _name='project.task.sec.sign.rout'

    name=fields.Char('Désignation')
    my_sec_id=fields.Many2one('project.task.exe.design',string='Désignation')
    date=fields.Date('Date')
    caracteristique=fields.Text('Caractéristique')
    valeur=fields.Integer('Valeur')
    unite=fields.Char('Unité')
    valider=fields.Boolean('Valider')
    my_task_sec_sign_rout_id=fields.Many2one('project.task',string='Sécurité et Signalisations Routières')
class project_task_terr_gen(models.Model):
    _name='project.task.terr.gen'

    name=fields.Char('Désignation')
    my_terr_id=fields.Many2one('project.task.exe.design',string='Désignation')
    date=fields.Date('Date')
    caracteristique=fields.Text('Caractéristique')
    valeur=fields.Integer('Valeur')
    unite=fields.Char('Unité')
    valider=fields.Boolean('Valider')
    my_terr_gen_id=fields.Many2one('project.task',string='Terrassements Généraux')

class  project_task_exe_design(models.Model):
    _name='project.task.exe.design'

    name=fields.Char(string='Désignation')
    type_etape=fields.Selection([('trav_prepa','Travaux préparatoires'),('terr_gen','Terrassements généraux'),('chauss','Chaussées')
                                 ,('ass_ouv_prot','Assainissement ouvrages et Protections'),('sec_sign_rout','Sécurité et Signalisation routière')],string='Type')
    caracteristique=fields.Text(string='Caractéristique')
    unite=fields.Char('Unité')

class project_hr_point_jour(models.Model):
    _name='project.hr.point.jour'

    def my_stock(self):
        tab=[]
        tab.append((0,0,{'stock_title':'Stock Matin'}))
        tab.append((0,0,{'stock_title':'Stock Soir'}))
        return tab


    name=fields.Char(string='Référence')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    code_chantier=fields.Char(string='Code')
    gazoil=fields.Float(string='Gazoil')
    huile_moteur=fields.Float(string='Moteur')
    huile_verrin=fields.Float(string='Verrin')
    stock_title=fields.Char(string='stock')
    pos_potence=fields.Integer(string='Position Potence:Pk')
    car_potence=fields.Integer(string='Carrière Potence:Pk')
    ope_potence=fields.Integer(string='Opération en Cours:Pk')
    obs=fields.Text(string='Observation')
    bareme_gazoil=fields.Integer(string='Barème Gazoil')
    trav_exe=fields.Text(string='TRAVAUX EXECUTES')
    lepointeur=fields.Binary(string='Le pointeur')
    my_point_ids=fields.One2many('project.hr.point.jour','my_point_id',string='stock',default=my_stock)
    my_point_id=fields.Many2one('project.hr.point.jour',string='stock')
    my_perso_ids=fields.One2many('project.hr.point.perso','my_perso_id',string='tableau pointage')
    my_persing_ids=fields.One2many('project.hr.point.perso.chauff','my_persing_id',string='tableau pointage')
    my_persoud_ids=fields.One2many('project.hr.point.perso.soud','my_persoud_id',string='tableau pointage')

    @api.onchange('my_persing_ids')
    def onchanger(self):
        if my_persing_ids:
            self.my_persing_ids.matricule={domain: [('readonly', '=', 1)]}


class project_hr_point_jou(models.Model):
    _name='project.hr.point.jourr'



    def my_stock(self):
        tab=[]
        tab.append((0,0,{'name':'Stock Matin'}))
        tab.append((0,0,{'name':'Stock Soir'}))
        return tab

    name=fields.Char(string='Référence')
    date=fields.Date('Date')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    code_chantier=fields.Char(string='Code',related='chantier_id.code')
    gazoil=fields.Float(string='Gazoil')
    huile_moteur=fields.Float(string='Moteur')
    huile_verrin=fields.Float(string='Verrin')
    stock_title=fields.Char(string='stock')
    pos_potence=fields.Integer(string='Position Potence:Pk')
    car_potence=fields.Integer(string='Carrière Potence:Pk')
    ope_potence=fields.Integer(string='Opération en Cours:Pk')
    obs=fields.Text(string='Observation')
    bareme_gazoil=fields.Integer(string='Barème Gazoil')
    trav_exec=fields.Many2many('project.trav.exe',string='TRAVAUX EXECUTES')
    lepointeur=fields.Binary(string='Le pointeur')
    my_stock_ids=fields.One2many('project.hr.point.stock','my_stock_id',string='Stock',default=my_stock)
    my_perso_ids=fields.One2many('project.hr.point.perso','my_perso_id',string='tableau pointage')
    my_persing_ids=fields.One2many('project.hr.point.perso.chauff','my_persing_id',string='tableau pointage')
    my_persoud_ids=fields.One2many('project.hr.point.perso.soud','my_persoud_id',string='tableau pointage')
    user_connected=fields.Many2one('res.users',string="Utilisateur Connecté",compute='my_auto_id')
    id_compute=fields.Integer('project_id')
    affecto_ids=fields.One2many('project.fleet.affecto','affecto_id',string='Affectation')
    profil_ids=fields.One2many('project.hr.point.profil','profil_id',string='Profil')

    @api.depends('id_compute')
    def my_auto_id(self):
        self.user_connected= self.env.uid


    def runs_server(self):

            idss=[]
            idsse=[]
            vehi=[]
            i=[]
            y=[]
            tab=[]
            tab1=[]
            tab2=[]
            tab3=[]
            tab4=[]
            tab5=[]
            tab6=[]
            tab7=[]
            tab8=[]
            tab9=[]
            tab10=[]
            tab11=[]
            tab12=[]
            idis=[]
            comp=[]

            vehicule=0
            mat=''
            idi=[]
            effect=[]





            idss=self.env["project.project"].search([('state','=','open')])

            """
               idis=self.pool.get('project.hr').search(self.env.cr,self.env.uid,[],order='company_hr desc')
               idi=self.pool.get('project.hr').browse(cr,uid,idis)
            """


            for record in idss:

                comp=self.env["project.hr.company"].search([])
                for compa in comp:
                    idi=self.env["project.hr"].search([('company_hr.id','=',compa.id),('project_id.id','=',record.id)])
                    idi.sorted(key=lambda	r:	r.id,	reverse=True)
                    if len(idi)!=0:
                      """
                      for recording in idi:

                      idsse=self.env['project.hr.meca.affect.board'].search([('affecta_id.id','=',recording.id)])


                      idsse.sorted(key=lambda	r:	r.id,	reverse=True)
                        y=vehi and max(vehi)

                    """













                      for idsse in idi:


                       if  idsse.company_hr.id == 2 and idsse.incontrat==True:
                           if idsse.fleet_affecto_id.cat_id.type_idd.id == 12 and idsse.profession.id == 2:



                               tab.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id == 12 and idsse.profession.id != 2:

                               tab.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and idsse.profession.id == 2:

                               tab1.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and idsse.profession.id == 1:

                                 tab2.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))

                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and (idsse.profession.id in [(17),(29),(28)]):

                                 tab3.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'profession':idsse.profession.name,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and (idsse.profession.id in [(5),(6),(7),(8),(9)]):

                                 tab8.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'profession':idsse.profession.name,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and (idsse.profession.id not in [(5),(6),(7),(8),(9) ,(17),(29),(28)]):

                                 tab9.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'profession':idsse.profession.name,'design_matoss':idsse.fleet_affecto_id.id}))

                       elif  idsse.company_hr.id != 2 and idsse.incontrat==True:
                           if idsse.fleet_affecto_id.cat_id.type_idd.id == 12 and idsse.profession.id == 2:



                               tab4.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id == 12 and idsse.profession.id != 2:

                               tab4.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and idsse.profession.id == 2:

                               tab5.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and idsse.profession.id == 1:

                                 tab6.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and (idsse.profession.id != 1 or idsse.profession.id != 2):

                                 tab7.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'profession':idsse.profession.name,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and (idsse.profession.id in [(5),(6),(7),(8),(9)]):

                                 tab10.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'profession':idsse.profession.name,'design_matoss':idsse.fleet_affecto_id.id}))
                           elif idsse.fleet_affecto_id.cat_id.type_idd.id != 12 and (idsse.profession.id not in [(5),(6),(7),(8),(9) ,(17),(29),(28)]):

                                 tab11.append((0,0,{'perso_id':idsse.id,'matricule':idsse.matricule,'profession':idsse.profession.name,'design_matoss':idsse.fleet_affecto_id.id}))






                tab4.extend(tab5)
                tab.extend(tab1)
                tab.extend(tab4)
                tab2.extend(tab6)



                tab7.extend(tab10)
                tab7.extend(tab11)
                tab3.extend(tab8)
                tab3.extend(tab9)
                tab3.extend(tab7)
                tab3.sort(key=lambda  r:r[2].get("profession"),reverse=False)




                self.create({'name':str(record.code)+'/'+str(record.id).zfill(10)+'/'+fields.Date.to_string(datetime.today()),'date':fields.Date.to_string(datetime.now()),'chantier_id':record.id,'my_perso_ids':tab,'my_persing_ids':tab2,
                                                   'my_persoud_ids':tab3})







    def creating_auto_fich(self):

          self.runs_server()

          return True
class project_hr_affecto_fleet(models.Model):
    _name='project.hr.affecto.fleet'

    name=fields.Char('Affectation')
    date_alloc=fields.Date('Date d\'allocation')
    date_retrait=fields.Date('Date d\'allocation')
    affecto_id=fields.Many2one('project.fleet',string='Affectation')
    histo_affecta_hr_id=fields.Many2one('project.hr',string='Historrique Des Affectations')

class project_fleet_affecto_hr(models.Model):
    _name='project.fleet.affecto_hr'

    name=fields.Char('Affectation')
    personne_id=fields.Many2one('project.hr',string='Personne',delegate=True)
    date_alloc=fields.Date('Date d\'allocation')
    date_retrait=fields.Date('Date d\'allocation')
    isopen=fields.Boolean('Fermé')
    obs=fields.Text('Observation')
    histo_affect_id=fields.Many2one('project.fleet',string='Affectation')

class project_fleet_affecto(models.Model):
    _name='project.fleet.affecto'

    name=fields.Char('Affectation')
    personne_id=fields.Many2one('project.hr',string='Personne',delegate=True)
    date_alloc=fields.Date('Date d\'allocation')
    date_retrait=fields.Date('Date d\'allocation')
    affecto_id=fields.Many2one('project.fleet',string='Affectation')
class project_trav_exe(models.Model):
    _name='project.trav.exe'
    name=fields.Char('Travaux Exécutés')
class project_hr_point_stock(models.Model):
    _name='project.hr.point.stock'

    name=fields.Char('name')
    gazoil=fields.Float('Gazoil')
    huile_moteur=fields.Float('Huile Moteur')
    huile_verrin=fields.Float('Huile Verrin')
    my_stock_id=fields.Many2one('project.hr.point.jourr',string='Stock')


class project_hr_point_perso(models.Model):
    _name='project.hr.point.perso'


    name=fields.Char(string='Personne')
    my_perso_id=fields.Many2one('project.hr.point.jourr',string='Pointage')


    perso_id=fields.Many2one('project.hr',string='Personnel',delegate=True)
    matricule=fields.Char(string='Matricule')
    presence=fields.Integer(string='Présence')
    trav_effect=fields.Char(string='Travaux Effectués')
    nbr_hr=fields.Integer(string='N° Heure')
    design_matoss=fields.Many2one('project.fleet',string='Désignation Matériel')
    dot_gazoil=fields.Float(string='Dotation Gazoil L')
    dot_huile=fields.Float(string='Dotation Huile L')




    @api.onchange('perso_id')
    def changeme(self):
        if self.perso_id:
           self.matricule=self.perso_id.matricule
           self.design_matoss=self.perso_id.fleet_affecto_id.id
class project_hr_point_profil(models.Model):
    _name='project.hr.point.profil'

    name=fields.Char('ref')
    type_profil_id=fields.Many2one('project.hr.point.etape.profil',string='étape')
    dupk=fields.Float('Du Pk')
    aupk=fields.Float('Au Pk')
    total=fields.Float('total')
    profil_id=fields.Many2one('project.hr.point.jourr',string='profil')

    @api.onchange('dupk','aupk')
    def vchaf(self):
        if self.dupk!=0 and self.aupk!=0:
            if self.aupk<self.dupk:
                raise  ValidationError("Le Pk final ne doit pas être inférieure au pk initial")
            else:
               self.total=(self.aupk - self.dupk) *25





class project_hr_point_etape_profil(models.Model):
    _name='project.hr.point.etape.profil'

    name=fields.Char('Profil')





class project_hr_point_perso_chauff(models.Model):
    _name='project.hr.point.perso.chauff'

    name=fields.Char(string='Personne')
    perso_id=fields.Many2one('project.hr',string='Personnel',delegate=True)
    matricule=fields.Char(string='Matricule')
    presence=fields.Integer(string='Présence')
    trav_effect=fields.Char(string='Travaux Effectués')
    nbr_hr=fields.Integer(string='N° Heure')
    design_matoss=fields.Many2one('project.fleet',string='Désignation Matériel')
    dot_gazoil=fields.Float(string='Dotation Gazoil L')
    dot_huile=fields.Float(string='Dotation Huile L')
    profil_1=fields.Integer(string="1")
    profil_2=fields.Integer(string="2")
    voy_requis_1=fields.Integer(string="1")
    voy_requis_2=fields.Integer(string="2")
    rest_litr=fields.Float(string='Rest. Litres')
    my_persing_id=fields.Many2one('project.hr.point.jourr',string='Pointage')
    @api.onchange('perso_id')
    def changeme(self):
        if self.perso_id:
           self.matricule=self.perso_id.matricule




class project_hr_point_perso_soud(models.Model):
    _name='project.hr.point.perso.soud'

    name=fields.Char(string='Personne')
    perso_id=fields.Many2one('project.hr',string='Personnel',delegate=True)
    matricule=fields.Char(string='Matricule')
    presence=fields.Integer(string='Présence')
    trav_effect=fields.Char(string='Travaux Effectués')
    nbr_hr=fields.Integer(string='N° Heure')
    design_matoss=fields.Many2one('project.fleet',string='Désignation Matériel')
    dot_gazoil=fields.Float(string='Dotation Gazoil L')
    dot_huile=fields.Float(string='Dotation Huile L')
    profession=fields.Char('profession')
    my_persoud_id=fields.Many2one('project.hr.point.jourr',string='Pointage')

    @api.onchange('perso_id')
    def changeme(self):
        if self.perso_id:
           self.matricule=self.perso_id.matricule
           return {'readonly': {'nbr_hr': [('Diagne', '=',self.perso_id.nom )]}}


class project_hr_(models.Model):
    _name='project.hr'

    def get_lastnum(self):
        idss=[]
        my_gid=0
        idss=self.pool.get('project.hr').search(self.env.cr,self.env.uid,[])
        idd=(int(idss and max(idss)) + 1) or 1


        return idd
    name=fields.Char(string='Personne',compute='get_time')
    nom=fields.Char(string='Nom')
    prenom=fields.Char(string='Prénom')
    last_num=fields.Integer('Last Num',default=get_lastnum)
    matricule=fields.Char(string='Matricule',compute='get_mat',store=True)
    num_ci=fields.Float(string='Numéro d\' identité',digits=(13,0))
    tel=fields.Float(string='Télephone',digits=(25,0))
    profession=fields.Many2one('project.hr.profession',string='Profession')
    incontrat=fields.Boolean('Sous contrat',default=False)
    year=fields.Integer('Année')
    marque=fields.Char('Marque')
    hr_trav_dep=fields.Integer('Heure début')
    hr_trav_fin=fields.Integer('Heure de fin')
    project_id=fields.Many2one('project.project',domain=[('state','=','open')])
    company_hr=fields.Many2one('project.hr.company',string="Entreprise")
    affecta_ids=fields.One2many('project.hr.meca.affect.board','affecta_id',string='Affectation')
    fleet_affecto_id=fields.Many2one('project.fleet',compute='alouer')
    my_perso_jour_ids=fields.One2many('project.hr.fiche.jour.contrat.jour','my_perso_jour_id',string='Feuille de temps',compute='get_time')
    my_perso_jour_hr_ids=fields.One2many('project.hr.fiche.jour.contrat.jour.hr','my_perso_jour_hr_id',string='Feuille de temps',compute='get_time')
    state=fields.Selection([('enconcept','En Conception'),('incontrat','Sous Contrat'),('ferme','Fermé')],default='enconcept')
    date_beg_cont=fields.Date(string='Date Début')
    date_fin_cont=fields.Date(string='Date Fin')
    choix_contrat=fields.Selection([],string='Fiche de temps de  réference')
    montant=fields.Float('Montant',digits=(20,0))
    indice=fields.Selection([('j','Jour'),('h','Heures'),('m','Mois')])
    net_a_payer=fields.Float('Net à payer',digits=(20,0))
    valeur_ajout=fields.Float('Valeur ajouté',digits=(20,0))
    my_permihr_ids=fields.One2many('project.hr.fleet.permis','my_permihr_id',string='Permis')
    motif=fields.Text('Motif')
    filename_avatar=fields.Char('Filename')
    image_avatar=fields.Binary('Photo')
    nb_total=fields.Float('Total',digits=(20,0))
    num_seq_mat=fields.Integer('Numero matricule sous-traitant',compute='num_seq_matik')
    my_doc_ids=fields.One2many('project.hr.doc_medic','my_doc_id',string='Document Medical')
    personne_to_hr_ids=fields.One2many('project.hr.rapport_to_hr','personne_to_hr_id',compute='get_time',string='Rapport de chantier')
    personning_ids=fields.Many2many('project.hr.rapport','Rapport de chantier',compute='get_time')
    image_medium=fields.Binary('image_medium')
    histo_affecta_ids=fields.Many2many('project.hr.affecto.fleet',string='Véhcicules alloués',compute='get_time')
    situation_matri=fields.Selection([('c','Célibataire'),('m','Marié(e)'),('d','Divorcé(e)'),('s','Séparé(e)'),('v','Veuf,Veuve'),('no','Non Connu(e)')])
    adresse=fields.Text('Adresse')
    frais_ids=fields.Many2many('project.hr.frais.board',string='Note de frais',compute='get_time')
    type_benne=fields.Selection([('b','Benne'),('bi','Bi Benne'),('tri','Tri Benne')])
    type_benne=fields.Selection([('b','Benne'),('bi','Bi Benne'),('tri','Tri Benne')])
    type_benne=fields.Selection([('b','Benne'),('bi','Bi Benne'),('tri','Tri Benne')])

    histo_affecta_rectif_ids=fields.Many2many('project.fleet.affecto_hr',string='Véhcicules alloués',compute='get_time')



    @api.one
    @api.depends('project_id','image_avatar')
    def num_seq_matik(self):
        idss=[]
        x=1
        if self.project_id.id !=2:
          idss=self.env["project.hr"].search([('company_hr.id','!=',2)])
          for rec in idss:
              rec.num_seq_mat=x
              x+=1

        if self.image_avatar:
           image=self.image_avatar or False



           if self.env.context.get("bin_size"):
            # refetch the image with a clean context
            image = self.env["project.hr"].with_context({}).browse(self.id).image_avatar or False



           self.image_avatar= tools.image_resize_image_medium(image,size=(200,250)) or False
        












    @api.one
    @api.depends('date_beg_cont','date_fin_cont','montant','valeur_ajout','indice','my_perso_jour_ids','nom','prenom','profession')
    def get_time(self):
        tab=[]
        tab1=[]
        tab2=[]
        tabfinal=[]
        tabfinal1=[]
        idsse=[]
        proj=[]
        idss=[]
        idss1=[]
        idss2=[]
        total_hr=0
        x=0
        y=0
        z=0
        sup=0
        sup1=0
        sup2=0
        jr1=0
        jr2=0
        jr3=0
        rap=[]
        amp=[]
        amp1=[]






        if self.last_num!=0:
           if self.nom or self.prenom or self.profession:
               self.name=(self.profession.name or ' ')+' '+(self.prenom or ' ')+ ' '+ (self.nom or ' ') + ' '
           rap=self.env["project.hr.rapport"].search([('personne_id.last_num','=',self.last_num)])

           amp1= self.env["project.hr.frais.board"].search([('personne_id.last_num','=',self.last_num)])
           if len(amp1)!=0:
               self.frais_ids=amp1



           amp= self.env["project.fleet.affecto_hr"].search([('personne_id.last_num','=',self.last_num)])
           if len(amp)!=0:

                self.histo_affecta_rectif_ids=amp

           if len(rap)!=0:
             self.personning_ids=rap





        if self.date_beg_cont or self.date_fin_cont:



           proj=self.env["project.project"].search([('state','=','open')])
           idsse=self.env["project.hr"].search([('last_num','=',self.last_num)])
           for record in proj:
               tab1=[]
               tab2=[]

               x=0
               y=0
               z=0
               sup=0
               sup1=0
               sup2=0
               jr1=0
               jr2=0
               jr3=0

               idss=self.env["project.hr.point.perso"].search([('perso_id.last_num','=',self.last_num),('my_perso_id.chantier_id.id','=',record.id),('my_perso_id.date','>=',self.date_beg_cont),('my_perso_id.date','<=',self.date_fin_cont)])
               idss1=self.env["project.hr.point.perso.chauff"].search([('perso_id.last_num','=',self.last_num),('my_persing_id.chantier_id.id','=',record.id),('my_persing_id.date','>=',self.date_beg_cont),('my_persing_id.date','<=',self.date_fin_cont)])
               idss2=self.env["project.hr.point.perso.soud"].search([('perso_id.last_num','=',self.last_num),('my_persoud_id.chantier_id.id','=',record.id),('my_persoud_id.date','>=',self.date_beg_cont),('my_persoud_id.date','<=',self.date_fin_cont)])

               if len(idss)!=0 or len(idss1)!=0 or len(idss2)!=0:

                  x=sum(rec.nbr_hr if rec.nbr_hr <=8 else 8 for rec in idss) if len(idss)!=0 else 0
                  sup=sum((0 if rec.nbr_hr <=8 else rec.nbr_hr-8) for rec in idss) if len(idss)!=0 else 0
                  jr1=sum((1 if rec.nbr_hr !=0 else 0)for rec in idss) if len(idss)!=0 else 0

                  y=sum(rec.nbr_hr if rec.nbr_hr <=8 else 8 for rec in idss1) if len(idss1)!=0 else 0
                  sup1=sum((0 if rec.nbr_hr <=8 else rec.nbr_hr-8) for rec in idss1) if len(idss1)!=0 else 0
                  jr2=sum((1 if rec.nbr_hr !=0 else 0)for rec in idss1) if len(idss1)!=0 else 0

                  z=sum(rec.nbr_hr if rec.nbr_hr <=8 else 8 for rec in idss2) if len(idss2)!=0 else 0
                  sup2=sum((0 if rec.nbr_hr <=8 else rec.nbr_hr-8) for rec in idss2) if len(idss2)!=0 else 0
                  jr3=sum((1 if rec.nbr_hr !=0 else 0)for rec in idss2) if len(idss2)!=0 else 0


                  tabfinal.append((0,0,{'chantier':record.name,'nbr_jour':jr1+jr2+jr3,'hr_sup':sup+sup1+sup2,'hr_fonct':x+y+z,'total':sup1+sup2+sup+z+x+y}))

               idss=self.env["project.hr.point.perso"].search([('perso_id.last_num','=',self.last_num),('my_perso_id.chantier_id.id','=',record.id)])
               idss1=self.env["project.hr.point.perso.chauff"].search([('perso_id.last_num','=',self.last_num),('my_persing_id.chantier_id.id','=',record.id)])
               idss2=self.env["project.hr.point.perso.soud"].search([('perso_id.last_num','=',self.last_num),('my_persoud_id.chantier_id.id','=',record.id)])

               if len(idss)!=0 or len(idss1)!=0 or len(idss2)!=0:

                  x=sum(rec.nbr_hr if rec.nbr_hr <=8 else 8 for rec in idss) if len(idss)!=0 else 0
                  sup=sum((0 if rec.nbr_hr <=8 else rec.nbr_hr-8) for rec in idss) if len(idss)!=0 else 0
                  jr1=sum((1 if rec.nbr_hr !=0 else 0)for rec in idss) if len(idss)!=0 else 0

                  y=sum(rec.nbr_hr if rec.nbr_hr <=8 else 8 for rec in idss1) if len(idss1)!=0 else 0
                  sup1=sum((0 if rec.nbr_hr <=8 else rec.nbr_hr-8) for rec in idss1) if len(idss1)!=0 else 0
                  jr2=sum((1 if rec.nbr_hr !=0 else 0)for rec in idss1) if len(idss1)!=0 else 0

                  z=sum(rec.nbr_hr if rec.nbr_hr <=8 else 8 for rec in idss2) if len(idss2)!=0 else 0
                  sup2=sum((0 if rec.nbr_hr <=8 else rec.nbr_hr-8) for rec in idss2) if len(idss2)!=0 else 0
                  jr3=sum((1 if rec.nbr_hr !=0 else 0)for rec in idss2) if len(idss2)!=0 else 0


                  tabfinal1.append((0,0,{'chantier':record.name,'nbr_jour':jr1+jr2+jr3,'hr_sup':sup+sup1+sup2,'hr_fonct':x+y+z,'total':sup1+sup2+sup+z+x+y}))












        self.my_perso_jour_ids=tabfinal
        self.my_perso_jour_hr_ids=tabfinal1


        if self.montant or self.valeur_ajout or self.indice:
            if self.indice =='h' or self.indice=='':
               self.net_a_payer= (self.montant or 0 )*  sum(reca.total for reca in self.my_perso_jour_ids)+self.valeur_ajout or 0
            else:
               self.net_a_payer=(self.montant or 0 )*sum(reca.nbr_jour for reca in self.my_perso_jour_ids)+self.valeur_ajout or 0

    @api.one
    def fermer_contrat(self):
        if not self.date_cloture :
            res=[]
            res2=[]
            i=0
            self.write({'date_cloture':fields.date.today()})
            res2=self.env["project.hr"].search([('last_num','=',self.last_num)])
            for ress in res2:
                ress.write({'incontrat':False,'project_id':False,'state':'ferme'})
                self.affecta_id.state='ferme'


    @api.one
    def alouer(self):
        idss=[]
        tab=[]
        idss=self.env["project.fleet"].search([('personne_id.last_num','=',self.last_num)])
        if len(idss)!=0:
          tab.append((0,0,{'name':"yes"}))


          self.write({'histo_affecta_ids':tab})
          self.fleet_affecto_id=idss[0].id
    @api.one
    @api.depends('company_hr')
    def get_mat(self):
        idss=[]
        idss1=[]
        idsse=[]
        idss2=[]
        tab=[]
        tab1=[]
        tab2=[]
        tabfinal=[]
        proj=[]
        ch=''
        idd=0



        idsse=self.pool.get('project.hr').search(self.env.cr,self.env.uid,[])
        idd=(int(idsse and max(idsse)) + 1) or 1
        self.matricule="001/"+str(self.id or "").zfill(4) if self.company_hr.id==2 else "" if self.company_hr==False else "005/"+str(self.id or "").zfill(4)
        if self.company_hr:
              self.matricule="001/"+str(self.id or "").zfill(4) if self.company_hr.id==2  else "005/"+str(self.company_hr.name[:5] or "")+str(self.num_seq_mat or "").zfill(4)






    @api.one
    def renouveler(self):
        self.write({
        'state': 'incontrat','incontrat':True
        })
        self.state='incontrat'
    @api.one
    def fermer(self):
        self.write({
        'state': 'ferme','incontrat':False
         })

        self.state='ferme'
    """
    @api.one
    @api.depends('nom','prenom','profession')
    def get_name(self):

            if self.nom or self.prenom or self.profession:
               self.name=(self.profession.name or ' ')+' '+(self.prenom or ' ')+ ' '+ (self.nom or ' ') + ' '

    @api.one
    @api.constrains('num_ci', 'tel')
    def _check_description(self):
        message=''
        if len(str(self.tel)) <9 or self.tel==0:
            message='[Téléphone]'
        if len(str(self.num_ci))<13 or self.num_ci==0:
           message=message+' [Numéro D\'identité]'
        if message !='':
           raise Warning("Les champs suivants sont invalides : "+message )

           """
class doc_medical(models.Model):
    _name = 'project.hr.doc_medic'




    name=fields.Char('Reférence',compute='get_num')
    date=fields.Date('Date',default=fields.Date.to_string(datetime.now()))
    obs=fields.Text('Observation')
    up_odc=fields.Binary('Document')
    filename=fields.Char('Filename')
    my_doc_id=fields.Many2one('project.hr',string='Document Médical')
    @api.one
    def get_num(self):
        idss=[]
        x=1
        ch=''
        if self.date:

         ch=str(fields.Date.to_string(datetime.today()))+"/"+str(self.id).zfill(4)

         self.name=ch
class project_hr_rapport(models.Model):
    _name='project.hr.rapport'

    name=fields.Char('Référence')
    personne_id=fields.Many2one('project.hr','Personne')
    user_connected=fields.Many2one('res.users',compute='get_user')
    motif=fields.Text('Motif')
    up_motif=fields.Binary('Document de rapport')
    filename=fields.Char('Filename')
    chantier_id=fields.Many2one('project.project',domain=[('state','=','open')],string='Chantier')
    date=fields.Date('Date')


    @api.one
    def get_user(self):
        self.user_connected=self.env.uid
class project_hr_rapport_to_hr(models.Model):
    _name='project.hr.rapport_to_hr'

    name=fields.Char('Référence')
    personne_to_hr_id=fields.Many2one('project.hr','Personne')
    user_connected=fields.Many2one('res.users',compute='get_user')
    motif=fields.Text('Motif')
    up_motif=fields.Binary('Document de rapport')
    filename=fields.Char('Filename')
    chantier_id=fields.Many2one('project.project',domain=[('state','=','open')],string='Chantier')
    date=fields.Date('Date')


    @api.one
    def get_user(self):
        self.user_connected=self.env.uid




class project_hr_fleet_doc(models.Model):
    _name='project.hr.fleet.doc'

    def getref(self):
        i=1
        xx=0
        idss=[]
        idss=self.pool.get('project.hr.fleet.doc').search(self.env.cr,self.env.uid,[])
        if idss:
              i=(int(idss and max(idss)) + 1) or 1


        return str(i)+'/'+str(self.fleet_id.matricule or ' ')

    name=fields.Char(string='Référence',default=getref)
    fleet_id=fields.Many2one('project.fleet',string='Véhicule')





class project_hr_fleet_greycard(models.Model):
    _name='project.hr.fleet.greycard'

    name=fields.Char('Numéro')
    date_beg=fields.Date('Date Début')
    date_fin=fields.Date('Date Fin')
    pdf_up=fields.Binary('PDF Carte à Grise')
    my_greyfleet_id=fields.Many2one('project.fleet')
    filename=fields.Char('filename')
class project_hr_fleet_permis(models.Model):
    _name='project.hr.fleet.permis'

    name=fields.Char('Numéro')
    num_agre=fields.Char('N° Agrément')
    num_titulaire=fields.Float('N° Titulaire',digits=(20,0))
    num_licence=fields.Float('N° Licence',digits=(20,0))
    type_licence=fields.Many2one('project.hr.fleet.type.licence','Type Licence')
    pdf_up=fields.Binary('PDF Permis')
    date_licence=fields.Date('Date Licence')
    my_permifleet_id=fields.Many2one('project.fleet')
    my_permihr_id=fields.Many2one('project.hr')
    filename=fields.Char('filename')

class project_hr_fleet_permis_type_licence(models.Model):
    _name='project.hr.fleet.permis.type.licence'

    name=fields.Char('Type Licence')

class project_hr_fleet_insurance(models.Model):
    _name='project.hr.fleet.insurance'

    name=fields.Char('Numéro')
    date_beg=fields.Date('Date Début')
    date_fin=fields.Date('Date Fin')
    pdf_up=fields.Binary('PDF Assurance')
    assureur=fields.Char('Souscripteur')
    my_insufleet_id=fields.Many2one('project.fleet')
    filename=fields.Char('filename')
    num_police=fields.Float('N° Police',digits=(20,0))


    @api.one
    def make_alert_insu(self):

        idd=[]
        idde=[]
        idd=self.env['project.fleet'].search([('id','=',self.my_insufleet_id.id)])
        if len(idd)!=0:

           idd[-1].write({'alert_insu':False })



    @api.one
    def check_expiration(self):
      """ Tests whether production is done or not.
        @return: True or False
      """
      res = False
      ob=0
      str=''
      idss=[]
      idsse=[]
      if self.date_fin:


        idss=self.env['project.hr.fleet.insurance'].search([])
        if len(idss)!=0:
           if idss[-1].date_fin == fields.Date.today():

                  idsse=self.env['project.fleet'].search([('id','=',idss[-1].my_insufleet_id.id)])
                  if len(idsse)!=0:

                     idsse[-1].write({'alert_insu':True})



      return True




class project_hr_profession(models.Model):
    _name='project.hr.profession'

    name=fields.Char('Profession')

class project_fleet_camion(models.Model):
    _name='project.fleet.camion'

    name=fields.Char(string='Camion')
    fleet_id=fields.Many2one('project.fleet',string='Désignation Véhicule')
    matricule=fields.Char(string='Matricule')
    categorie=fields.Char(string='Catégorie/Modèle',related='fleet_id.cat_id.name')
    my_fleet_cam_id=fields.Many2one('project.task',string='Camion')
    ch=fields.Integer('Heure marche')
    etat=fields.Selection([('1','Marche'),('2','Immobile'),('3','Panne')],string='Etat')
    nbr_load=fields.Integer(string='Nombre de Chargement')
    kilo_by_load=fields.Integer(string='Kilomètres par chargement')
    date_dot=fields.Date('Date Dotation')
    dot_huile=fields.Float(string='Dot. Huile')
    dot_gazoil=fields.Float(string='Dot. Gazoil')
    trav_exe=fields.Text('Travaux Exécutés')
    panne_id=fields.Many2one('project.fleet.panne',string='Panne')
    obs=fields.Text('Observation')


class project_fleet_engine(models.Model):
    _name='project.fleet.engine'

    name=fields.Char(string='Engin')
    fleet_id=fields.Many2one('project.fleet',string='Désignation Véhicule')
    matricule=fields.Char(string='Matricule')
    categorie=fields.Char(string='Catégorie/Modèle',related='fleet_id.cat_id.name')
    my_fleet_eng_id=fields.Many2one('project.task',string='Engin')
    regime=fields.Char('Régime')
    dot_huile=fields.Float(string='Dot. Huile')
    hr_march=fields.Integer(string='Heure marche')
    dot_gazoil=fields.Float(string='Dot. Gazoil')
    etat=fields.Selection([('1','Marche'),('2','Immobile'),('3','Panne')],string='Etat')
    date_dot=fields.Date(string='Date Dotation')
    trav_exe=fields.Text('Travaux Exécutés')
    panne_id=fields.Many2one('project.fleet.panne',string='Panne')
    obs=fields.Text('Observation')

class project_fleet_pannne(models.Model):
    _name='project.fleet.panne'

    name=fields.Char('Pannne')
class project_fleet_big_cat(models.Model):
    _name='project.fleet.big_cat'


    name=fields.Char(string='Catégorie')
    type_idd=fields.Many2one('project.fleet.type',string='Type')

class project_fleet_cat(models.Model):
    _name='project.fleet.cat'

    name=fields.Char(string='Sous Catégorie')
    type_idd=fields.Many2one('project.fleet.big_cat',string='Catégorie')
    photo=fields.Binary('Photo')

class project_fleet_type(models.Model):
    _name='project.fleet.type'

    name=fields.Char(string='Type')
class project_fleet_cat(models.Model):
    _name='project.fleet.model'

    name=fields.Char(string='Model')
    cat_id=fields.Many2one('project.fleet.cat',string='Catégorie')
class project_fleet(models.Model):
    _name='project.fleet'

    name=fields.Char(string='Véhicule',compute='get_ref')
    type_id=fields.Many2one('project.fleet.type',string='Type')
    cat_id=fields.Many2one('project.fleet.cat',string='Catégorie')
    model_id=fields.Many2one('project.fleet.model',string='Model')
    matricule=fields.Char(string='Matricule')
    reference=fields.Char('Référence',compute='get_ref')
    doc_count=fields.Integer(string='Nombre de pièces Administratives',compute='all_count')
    vidange_survey=fields.Char(string='Delai limite vidange atteint')
    personne_id=fields.Many2one('project.hr',string='Affecté à',domain=[('profession.name','in',['Chauffeur','Conducteur'])])
    photo_up1=fields.Binary('Photo')
    photo_up2=fields.Binary('Photo')
    photo_up3=fields.Binary('Photo')
    photo_up4=fields.Binary('Photo')
    photo_up5=fields.Binary('Photo')
    photo_up6=fields.Binary('Photo')
    date_dacquis=fields.Date('Date d\'aquisition')
    marque=fields.Char('Marque')
    origine=fields.Char('Origine')
    huile_moteur=fields.Float('Huile Moteur')
    huile_verrin=fields.Float('Huile Verrin')
    cartouch_ids=fields.One2many('project.fleet.cartouche','cartouch_id',string='Liste des Cartouches')
    flexible_ids=fields.One2many('project.fleet.flexible','flexible_id',string='Liste des Flexibles')
    struct_ids=fields.One2many('project.fleet.structure','struct_id',string='Structure')
    delai_entretien=fields.Float('Delai Maximal d\'entretien',digits=(16,0))
    grand_entretien=fields.Text('Grand entretien')
    livr_entretien=fields.Binary('Livret d\'entretien et d\'instruction')
    type_pneu=fields.Many2one('project.fleet.type_pneu',string='Type Pneu')
    big_cat_id=fields.Many2one('project.fleet.big_cat',compute='get_ref',store=True,string='Catégorie')
    bande_roulement=fields.Char('Bande de roulement')
    diametre=fields.Float('Diamètre')
    tire_conception=fields.Char('Tire de conception')
    company=fields.Many2one('project.hr.company',string='Entreprise')
    my_sstraitant_id=fields.Many2one('project.hr.ss_traitant',string='Entreprise')
    filename1=fields.Char('filename')
    filename2=fields.Char('filename')
    filename3=fields.Char('filename')
    filename4=fields.Char('filename')
    filename5=fields.Char('filename')
    filename6=fields.Char('filename')
    type_moteur=fields.Many2one('project.fleet.moteur')
    my_insufleet_ids=fields.One2many('project.hr.fleet.insurance','my_insufleet_id',string='Assurance')
    my_greyfleet_ids=fields.One2many('project.hr.fleet.greycard','my_greyfleet_id',string='Carte à Grise')
    my_permifleet_ids=fields.One2many('project.hr.fleet.permis','my_permifleet_id',string='Permis')
    alert_insu=fields.Boolean('Assurance à Jour',default=False)
    alert_greycard=fields.Boolean('Carte à grise',default=False)
    histo_affect_ids=fields.One2many('project.fleet.affecto_hr','histo_affect_id',string='Véhcicules alloués')



    @api.one
    def check_alert_insu(self):
        idss=[]
        idsse=[]


        idss=self.env['project.hr.fleet.insurance'].search([])
        if len(idss)!=0:

           if idss[-1].date_fin==fields.Date.today():

              self.write({'alert_insu':True})


    @api.multi
    def all_count(self):
        res=[]
        a=0
        res=self.env['project.hr.fleet.doc'].search([])

        for x in res:
            if(x.fleet_id.name==self.name):

                a=a+1

        self.doc_count=a

    @api.one
    @api.depends('matricule','cat_id','model_id','my_sstraitant_id','photo_up1','photo_up2','photo_up3','photo_up4','photo_up5','photo_up6','reference')
    def get_ref(self):
        tab=[]
        res=[]
        res1=[]
        last_id=[]
        last_id=self.env['project.hr'].search([])
        self.big_cat_id=self.cat_id.type_idd.id or False

        self.reference="002/"+str(self.id or 0).zfill(6) if (self.big_cat_id.type_idd.id  <=3 and self.company.id ==2) else "003/"+str(self.id or 0).zfill(6) if (self.big_cat_id.type_idd.id ==4
                 and  self.company.id  ==2) else "004/"+str(self.id or 0).zfill(6) if (self.big_cat_id.type_idd  ==5 and self.company.id ==2) else "006/"+str(self.id or 0).zfill(6) if (self.big_cat_id.type_idd.id  <=3 and self.company.id !=2) else ""

        if self.matricule or self.model_id:
            self.name=(self.cat_id.name + ' ' if self.cat_id else '') + (self.matricule + ' ' if self.matricule else '')
        if self.cat_id:

               self.big_cat_id=self.cat_id.type_idd.id
               res=self.env['project.fleet.structure'].search([('big_cat.id','=',self.cat_id.type_idd.id)])
               res1=self.env['project.fleet.cat'].search([('id','=',self.cat_id.id)])
               if len(res1)!=0:
                   self.photo_up1=res1[0].photo
               if len(res)!=0:
                  for record in res:
                      tab.append((0,0,{'name':record.name,'photo':record.photo}))
               self.struct_ids=tab
        if self.my_sstraitant_id:
            self.company=self.my_sstraitant_id.my_comp_ids.id
            if self.my_sstraitant_id!=False:
               self.reference="002/"+str(self.id or 0).zfill(6) if (self.big_cat_id.type_idd.id  <=3 and self.company.id ==2) else "003/"+str(self.id or 0).zfill(6) if (self.big_cat_id.type_idd.id ==4
                 and  self.company.id  ==2) else "004/"+str(self.id or 0).zfill(6) if (self.big_cat_id.type_idd  ==5 and self.company.id ==2) else "006/"+str(self.id or 0).zfill(6)


        if self.photo_up1 or self.photo_up2 or self.photo_up3 or self.photo_up4 or self.photo_up5 or self.photo_up6:
           image=self.photo_up1 or False
           image1=self.photo_up2 or False
           image2=self.photo_up3 or False
           image3=self.photo_up4 or False
           image4=self.photo_up5 or False
           image5=self.photo_up6 or False

           if self.env.context.get("bin_size"):
            # refetch the image with a clean context
            image = self.env[self._name].with_context({}).browse(self.id).photo_up1 or False
            image1 = self.env[self._name].with_context({}).browse(self.id).photo_up2 or False
            image2 = self.env[self._name].with_context({}).browse(self.id).photo_up3 or False
            image3 = self.env[self._name].with_context({}).browse(self.id).photo_up4 or False
            image4 = self.env[self._name].with_context({}).browse(self.id).photo_up5 or False
            image5 = self.env[self._name].with_context({}).browse(self.id).photo_up6 or False

            data = tools.image_get_resized_images(image) or False
           self.photo_up1= tools.image_resize_image_medium(image ,size=(300,300)) or False
           self.photo_up2= tools.image_resize_image_medium(image1,size=(300,300)) or False
           self.photo_up3= tools.image_resize_image_medium(image2 ,size=(350,350)) or False
           self.photo_up4= tools.image_resize_image_medium(image3,size=(350,350)) or False
           self.photo_up5= tools.image_resize_image_medium(image4,size=(350,350)) or False
           self.photo_up6= tools.image_resize_image_medium(image5,size=(350,350)) or False

    @api.v7
    def return_action_to_open(self, cr, uid, ids, context=None):
        """ This opens the xml view specified in xml_id for the current vehicle """
        if context is None:
            context = {}
        if context.get('xml_id'):
            res = self.pool.get('ir.actions.act_window').for_xml_id(cr, uid ,'project', context['xml_id'], context=context)
            res['context'] = context
            res['context'].update({'default_fleet_id': ids[0]})
            res['domain'] = [('fleet_id','=', ids[0])]
            return res
        return False



class project_fleet_type_pneu(models.Model):
    _name='project.fleet.type_pneu'

    name=fields.Char('Type Pneu')


class project_fleet_cartouch(models.Model):
     _name='project.fleet.cartouche'

     name=fields.Char('Cartouche')
     reference=fields.Char('Reference')
     type_cartouche=fields.Many2one('project.fleet.type.cartouche',string='Type Cartouche')
     photo=fields.Binary('Photo')
     cartouch_id=fields.Many2one('project.fleet')
class project_fleet_type_cartouche(models.Model):
    _name='project.fleet.type.cartouche'

    name=fields.Char('Type')

class project_fleet_flexible(models.Model):
    _name='project.fleet.flexible'

    name=fields.Char('Flexible')
    emplacement=fields.Char('Emplacement')
    reference=fields.Char('Réference')
    photo=fields.Binary('Photo')
    flexible_id=fields.Many2one('project.fleet',string='Flexible')

class project_fleet_structure(models.Model):
    _name='project.fleet.structure'

    name=fields.Char('Désignation')
    photo=fields.Binary('Photos')
    cat=fields.Many2one('project.fleet.cat',string='Catégorie')
    big_cat=fields.Many2one('project.fleet.big_cat',string='Catégorie')
    valeur=fields.Char('Valeur')
    struct_id=fields.Many2one('project.fleet')
    filename=fields.Char('Filename')
class project_hr_frais(models.Model):
    _name='project.hr.frais'

    name=fields.Char('Désignation',compute='ref')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    user_connected=fields.Many2one('res.users',string='Utilisateur Connecté',computed='ref')
    frais_ids=fields.One2many('project.hr.frais.board','frais_id',string='Note de frais')



    @api.one
    def ref(self):
        self.user_connected=self.env.uid

        self.name=str(self.chantier_id.code or 0)+'/'+str(self.chantier_id.id or 0).zfill(4)+'/'+fields.Date.to_string(datetime.today())


class project_hr_frais_board(models.Model):
    _name='project.hr.frais.board'

    name=fields.Char('Désignation')
    personne_id=fields.Many2one('project.hr',string='Personne')
    type_frais=fields.Many2one('project.hr.type.frais',string='Type de frais')
    chantier=fields.Char('Chantier',related='frais_id.chantier_id.name',compute='name_chantier')
    montant=fields.Float(string='Montant',digits=(20,0))
    date=fields.Date('Date')
    frais_id=fields.Many2one('project.hr.frais',string='Note de frais')
    obs=fields.Text('Observation')
    @api.one
    @api.depends('frais_id')
    def name_chantier(self):
        if self.frais_id:
           self.chantier=self.frais_id.chantier_id.name

class project_hr_type_frais(models.Model):
    _name='project.hr.type.frais'


    name=fields.Char('Type de frais')




class project_fleet_entretien(models.Model):
    _name='project.fleet.entretien'

    name=fields.Char('Entretien')
    categorie=fields.Many2one('project.fleet.cat','Catégorie')
    deroulement=fields.Text('Déroulement')




class  project_hr_fleet_vidange(models.Model):
      _name='project.hr.fleet.vidange'

      name=fields.Char(string='Référence')
      fleet_id=fields.Many2one('project.fleet',string='Véhicule')
      my_board_ids=fields.One2many('project.hr.fleet.vidange.board','my_board_id',string='Tableau')
      state=fields.Selection([('a','Delai limite'),('n','Normal')])
      hr_fonct=fields.Integer('Nombre D\'heures D\'activité',compute='get_hr')
      @api.depends('my_board_ids')
      def get_hr(self):
        res=[]
        self.env['project.hr.fiche.jour.board'].search([('my_id.fleet_id.name','=',self.fleet_id.name),('','=',)])

class project_hr_fleet_vidange(models.Model):
      _name='project.hr.fleet.vidange.board'

      name=fields.Char('Tableau')
      date_vidange=fields.Date('Date Vidange')
      pdf_up=fields.Binary(string='PDF Etat')
      obs=fields.Text('Observation')
      my_board_id=fields.Many2one('project.hr.fleet.vidange',string='Tableau')



class project_hr_point_hebdo(models.Model):
      _name='project.hr.point.hebdo'



      name=fields.Char(string='Référence',compute='getref')
      mois=fields.Date(string='Mois')
      chantier_id=fields.Many2one('project.project',string='Chantier')
      date_beg=fields.Date(string='Semaine du')
      date_fin=fields.Date(string='Au')
      my_point_ids=fields.One2many('project.hr.point.hebdo.timesheet','my_point_id',string='Tableau de pointage')
      miss_ctrl=fields.Binary(string='La mission de contrôle')
      user_connected=fields.Many2one('res.users',string='Utilisateur Connecté')





      @api.depends('date_beg','chantier_id')
      def getref(self):
          idd=0
          idss=[]
          idss=self.pool.get('project.hr.point.hebdo').search(self.env.cr,self.env.uid,[])
          idd=(idss and max(idss) + 1 )or 1
          ch=str(idd)
          if self.date_beg:
              self.date_fin=fields.Date.to_string(fields.Date.from_string(self.date_beg)+ timedelta(days=6))
              self.name= self.date_beg
          if self.chantier_id:
              self.name=ch+'/'+(self.chantier_id.name or ' ') + '/'+ (self.date_beg or ' ')


class project_hr_point_hebdo_timesheet(models.Model):
      _name='project.hr.point.hebdo.timesheet'

      name=fields.Char(string='Timesheet')
      my_point_id=fields.Many2one('project.hr.point.hebdo',string='Tableau de pointage')
      personne_id=fields.Many2one('project.hr',string='Prénom et Nom')
      matricule=fields.Char(string='Matricule',related='personne_id.matricule')
      emp_cat=fields.Char(string='Emploi-Catégorie',related='personne_id.profession.name')
      lundi=fields.Integer(string='Lundi')
      mardi=fields.Integer(string='Mardi')
      mercredi=fields.Integer(string='Mercredi')
      jeudi=fields.Integer(string='Jeudi')
      vendredi=fields.Integer(string='Vendredi')
      samedi=fields.Integer(string='Samedi')
      dimanche=fields.Integer(string='Dimanche')
      total_hrpoint=fields.Integer(string='HP')
      total_hrsup=fields.Integer(string='HS')

      @api.onchange('personne_id','lundi','mardi','mercredi','jeudi','vendredi','samedi','dimanche')
      def changepers(self):
          if self.my_point_id.my_point_ids.personne_id:
              self.my_point_id.my_point_ids.emp_cat=self.my_point_id.my_point_ids.personne_id.profession.name or ' '
              self.my_point_id.my_point_ids.matricule=self.my_point_id.my_point_ids.personne_id.matricule or ' '
          if self.lundi or self.mardi or self.mercredi or self.jeudi or self.vendredi or self.samedi or self.dimanche:
              self.total_hrpoint= (self.lundi if self.lundi <=8 else 0)+(self.mardi if self.mardi <=8 else 0)+(self.mercredi if self.mercredi <=8 else 0)+(self.jeudi if self.jeudi <=8 else 0)+(self.vendredi if self.vendredi <=8 else 0)+(self.samedi if self.samedi <=8 else 0)+(self.dimanche if self.dimanche <=8 else 0)
              self.total_hrsup= (self.lundi-8 if self.lundi >8 else 0)+(self.mardi-8 if self.mardi >8 else 0)+(self.mercredi-8 if self.mercredi >8 else 0)+(self.jeudi-8 if self.jeudi >8 else 0)+(self.vendredi-8 if self.vendredi >8 else 0)+(self.samedi-8if self.samedi >8 else 0)+(self.dimanche-8 if self.dimanche >8 else 0)








class project_task_cmd_matos(models.Model):
     _name='project.task.cmd.matos'

     name=fields.Char(string='Matériaux')
     quantite=fields.Integer(string='Quantité')
     unite=fields.Char(string='Unité')
     date_mise=fields.Date(string='Date Mise en Place')
     obs=fields.Text(string='Observation')
     user_connected=fields.Many2one('res.users',string='Utilisateur Connecté')
     my_matos_cmd_id=fields.Many2one('project.task',string='Materiaux/Commandes')

class project_task_cmd_matos_design(models.Model):
      _name='project.task.cmd.matos.design'

      name=fields.Char('Matériaux')
      unite=fields.Char(string='Unité')

class project_task_topo(models.Model):
      _name='project.task.topo'

      name=fields.Char(string='Tableau Topographie')
      nb_prof=fields.Char(string='NB Numéro de profil')
      lect_arr=fields.Float(string='(LAR) Lecture Arrière')
      lect_av=fields.Float(string='(LAV) Lecture Avant')
      cote_terr=fields.Float(string='(COTE) Cote sur terrain')
      cote_proj=fields.Float(string='Cote Projet')
      diff_pos=fields.Float(string='+')
      diff_nega=fields.Float(string='-')
      obs=fields.Text(string='Observation')


class project_hr_fiche_jour(models.Model):
      _name='project.hr.fiche.jour'


      name=fields.Char(string='Réference',compute='myref')
      chantier_id=fields.Many2one('project.project',string='Chantier')
      fonction=fields.Char(string='Fonction',compute='myref')
      personne_id=fields.Many2one('project.hr',string='Prénom et Nom')
      matricule=fields.Char(string='N°',related='personne_id.matricule')
      date=fields.Date(string='Date',default=fields.Date.to_string(datetime.now()))
      mois=fields.Char(string='Mois',compute='onchangeme')
      my_ids=fields.One2many('project.hr.fiche.jour.board','my_id',string='Tableau',compute='comp_id',store=True)
      chefchantier=fields.Binary(string='Chef de chantier')
      chauffeur=fields.Binary(string='Le Chauffeur')
      fleet_id=fields.Many2one('project.fleet',string='Matricule')
      pointeur=fields.Binary(string='Le Pointeur')
      specialist=fields.Binary(string='Le Spécialiste')
      maneuvre=fields.Binary(string='Le Manoeuvre')
      user_connected=fields.Many2one('res.users',string='Utilisateur Connecté',compute='my_auto_id')
      @api.one
      def myref(self):
          self.name= str(self.chantier_id.code)+'/'+str(self.id or 0).zfill(10)
          self.fonction= str(self.personne_id.profession.name or ' ') + ' ' + (('('+str(self.personne_id.company_hr.name) +')') or ' ')
      def my_auto_id(self):
        self.user_connected= self.env.uid

      def comp_id(self):

              int_mois=0
              int_year=0
              daye=datetime.now()
              datetime1=datetime.now()
              date=fields.Date()
              date2=fields.Date()
              date1=fields.Date()
              datedebut=fields.Date()
              mytimedelta=timedelta(days=1)
              tab=[]
              tabperso=[]
              tabchauff=[]
              tabsoud=[]
              date=datetime.now()
              int_mois=int(date.month)
              int_year=int(date.year)
              datedebut=datetime(int_year,int_mois-1,26)
              date2=datetime(int_year,int_mois,26)

              while datedebut < date2:
                  date1=fields.Date.to_string(datedebut)
                  """
                  tabperso=self.env["project.hr.point.perso.chauff"].search([('perso_id.id','=',self.personne_id.id),('my_persing_id.date','=',date1)])
                  """
                  tab.append((0,0,{'jour':date1,'gazoil':tabperso[0].dot_gazoil if len(tabperso) != 0 else 0}))

                  datedebut=datedebut + timedelta(days=1)
              self.my_ids=tab


      @api.one
      @api.depends('create_date','mois')
      def onchangeme(self):


            if self.create_date!='':

              moiss=''
              int_mois=0
              int_year=0
              daye=datetime.now()
              datetime1=datetime.now()
              date=fields.Date()
              date2=fields.Date()
              date1=fields.Date()
              datedebut=fields.Date()
              mytimedelta=timedelta(days=1)
              tab=[]
              tabperso=[]
              tabchauff=[]
              tabsoud=[]







              date=fields.Date.from_string(self.create_date)
              int_mois=int(date.month)
              int_year=int(date.year)

              daye=date.day

              moiss= 'Janvier' if (int_mois == 1) else ('Fevrier' if (int_mois == 2) else ('Mars' if (int_mois == 3) else('Avril' if (int_mois == 4) else
                    ('Mai' if (int_mois == 5) else ('Juin' if (int_mois == 6) else('Juillet' if (int_mois == 7) else ('Aout' if (int_mois == 8) else('Septembre' if (int_mois == 9) else('Octobre' if (int_mois == 10) else('Novembre' if (int_mois == 11) else 'Decembre'))))))))))

              self.mois=moiss




class project_hr_fiche_jour_board(models.Model):
    _name='project.hr.fiche.jour.board'

    name=fields.Char('Personne')
    jour=fields.Date(string='Date')
    gazoil=fields.Float(string='Gazoil',compute='get_val')
    huile=fields.Float(string='Huile')
    nbr_jour=fields.Integer(string='Nombre de J')
    hr_dep=fields.Integer(string='H. Départ',related='my_id.personne_id.hr_trav_dep')
    hr_darr=fields.Integer(string='H. d\'arriv',related='my_id.personne_id.hr_trav_fin')
    hr_fonct=fields.Integer(string='H. Fonct')
    hr_supp=fields.Integer(string='H. Suppl')
    decharge=fields.Char(string='Décharge')
    obs=fields.Text(string='Observation')
    my_id=fields.Many2one('project.hr.fiche.jour',string='Tableau')
    @api.one
    def get_val(self):
        idss=[]
        idss1=[]
        idss2=[]
        diff=0
        idss=self.env["project.hr.point.perso"].search([('perso_id.id','=',self.personne_id.id),('my_perso_id.date','=',self.jour)])
        idss1=self.env["project.hr.point.perso.chauff"].search([('perso_id.id','=',self.personne_id.id),('my_persing_id.date','=',self.jour)])
        idss2=self.env["project.hr.point.perso.soud"].search([('perso_id.id','=',self.personne_id.id),('my_persoud_id.date','=',self.jour)])
        if len(idss)!=0 or len(idss1)!=0  or len(idss2)!=0:

           self.gazoil=(sum(rec.dot_gazoil for rec in idss) or 0) + (sum(reca.dot_gazoil for reca in idss1) or 0) + (sum(reco.dot_gazoil for reco in idss2) or 0)
           self.huile=(sum(rec.dot_huile for rec in idss) or 0) + (sum(reca.dot_huile for reca in idss1 ) or 0) + (sum(reco.dot_huile for reco in idss2) or 0)
           self.nbr_jour=(sum(rec.presence for rec in idss) or 0) + (sum(reca.presence for reca in idss1 ) or 0)+ (sum(reco.presence for reco in idss2) or 0)
           self.hr_fonct=(sum(rec.nbr_hr for rec in idss) or 0) + (sum(reca.nbr_hr for reca in idss1 ) or 0) + (sum(reco.nbr_hr for reco in idss2) or 0)


           self.hr_dep=self.my_id.personne_id.hr_trav_dep
           self.hr_darr=self.my_id.personne_id.hr_trav_fin
           diff=self.hr_darr-self.hr_dep
           self.hr_supp = self.hr_fonct - diff if (self.hr_fonct > diff) else 0


           self.obs= (sum(rec.trav_effect for rec in idss) or 0) + (sum(reca.trav_effect for reca in idss1 ) or 0 )+ (sum(reco.trav_effect for reco in idss2) or 0)

    """
    @api.onchange('hr_dep','hr_darr')
    def onchanges(self):
        if self.hr_dep and self.hr_darr:
              if self.my_id.my_ids.hr_dep >= self.my_id.my_ids.hr_darr:
                 raise ValidationError('L\'heure de départ ne peut pas être supérieure à l\'heure d\'arrivée' )
              self.my_id.my_ids.hr_fonct=8 if self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep>=8 else self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep
              self.my_id.my_ids.hr_supp=0 if  self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep<=8 else self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep - 8
    """
class project_hr_fiche_jour_contrat(models.Model):
    _name='project.hr.fiche.jour.contrat'


    def gest_num(self):
        idss=[]
        ch=''
        my_id=0
        idss=self.pool.get('project.hr.fiche.jour.contrat').search(self.env.cr,self.env.uid,[])
        if idss:

           my_id=(int(idss and max(idss)) + 1) or 1
           ch=str(self.personne_id.matricule or '')+'/'+str(self.create_date or '')+'/PAIE'+str(my_id)

        return ch

    name=fields.Char(string='Référence',default=gest_num)
    date_debut=fields.Date(string='Date Début',default=fields.Date.to_string(datetime(int(fields.Date.from_string(fields.Date.today()).year),int(fields.Date.from_string(fields.Date.today()).month)-1,26)))
    chantier_id=fields.Many2one('project.project',string='Chantier')
    personne_id=fields.Many2one('project.hr',string='Prénom et Nom')
    date_fin=fields.Date(string='Date Fin',default=fields.Date.to_string(datetime(int(fields.Date.from_string(fields.Date.today()).year),int(fields.Date.from_string(fields.Date.today()).month),25)))
    montant=fields.Float(sting='Montant')
    indice=fields.Selection([('h','Heure'),('j','Jour')])
    tableau_ids=fields.One2many('project.hr.fiche.jour.contrat','tableau_id',string='Tableau')
    tableau_id=fields.Many2one('project.hr.fiche.jour.contrat',string='tableau')
    my_jour_ids=fields.One2many('project.hr.fiche.jour.contrat.jour','my_jour_id',string='fiche journalière')
    my_meca_ids=fields.One2many('project.hr.fiche.jour.contrat.meca','my_meca_id',string='fiche mécanique')
    my_hebdo_ids=fields.One2many('project.hr.fiche.jour.contrat.hebdo','my_hebdo_id',string='fiche mécanique')
    valeur_ajout=fields.Float('Valeur Ajouté')
    motif=fields.Text(string='Motif')
    choix_contrat=fields.Selection([('pointjour','Pointage Journalière'),('pointmeca','Pointage Journalier Mécanique'),('pointhebdo','Pointage Hebdomadaire')])
    nb_total=fields.Integer(string='Nombre Heures Total',compute='_compute_total')
    type_contrat=fields.Many2one('project.hr.profession',related='personne_id.profession')
    net_payer=fields.Float('Net à Payer')
    etat_contrat=fields.Selection([('sousconcept','En conception'),('souscontrat','Sous Contrat'),('ferme','Fermé')],default='sousconcept')

    @api.depends('my_jour_ids')
    def _compute_total(self):
        for record in self:
            record.nb_total = sum(line.total for line in record.my_jour_ids)
    @api.one
    def renouveler(self):
        self.write({
        'etat_contrat': 'souscontrat',
        })
    @api.one
    def fermer(self):
        self.write({
        'etat_contrat': 'ferme',
         })

    @api.multi
    @api.onchange('montant','indice','date_debut','date_fin','choix_contrat','personne_id','valeur_ajout')
    def gest_contrat(self):
        idss=[]
        idsse=[]
        tab=[]
        ide=[]
        record=[]
        self.tableau_ids=tab
        if self.montant or self.valeur_ajout or self.indice:
            if self.indice=='h' or self.indice=='':
               self.net_payer=(self.montant or 0 )*sum(reca.total for reca in self.my_jour_ids or False)+self.valeur_ajout or 0
            else:
               self.net_payer=(self.montant or 0 )*sum(reca.nbr_jour for reca in self.my_jour_ids or False)+self.valeur_ajout or 0



        if self.personne_id:

           if self.personne_id!=False:
              if self.date_debut !='' or self.date_fin !='':
                 ide=self.pool.get('project.hr.meca.affect.board').search(self.env.cr,self.env.uid,[('my_affect_id.personne_id.id','=',self.personne_id.id),('date_affect', '>=',self.date_debut)])
                 record=self.pool.get('project.hr.meca.affect.board').browse(self.env.cr,self.env.uid,ide)
                 for recing in record:
                     if self.personne_id.profession.name=='Chauffeur':
                        idss=self.pool.get('project.hr.point.perso').search(self.env.cr,self.env.uid,[('perso_id.id','=',self.personne_id.id or False),
                                                                                             ('my_perso_id.date','>=',self.date_debut),('my_perso_id.date','<=',self.date_fin)])
                        idsse=self.pool.get('project.hr.fiche.jour.board').browse(self.env.cr,self.env.uid,idss)
                        tab.append([(0,0,{'chantier':recing.chantier_id.name,'nbr_jour':len(idss),'hr_fonct':sum(res.nbr_hr if res.nbr_hr <8 else 8  for res in idsse),

                                          'hr_sup':sum(res.nbr_hr - 8 if res.nbr_hr >8 else 0 for res in idsse),'total':sum(res.nbr_hr if res.nbr_hr <8 else 8  for res in idsse)+
                                                       sum(res.nbr_hr - 8 if res.nbr_hr >8 else 0 for res in idsse)})])


                     elif self.personne_id.profession.name=='Conducteur':
                          idss=self.pool.get('project.hr.point.perso.chauff').search(self.env.cr,self.env.uid,[('perso_id.id','=',self.personne_id.id or False),
                                                                                                    ('my_persing_id.date','>=',self.date_debut),('my_persing_id.date','<=',self.date_fin)])
                          idsse=self.pool.get('project.hr.fiche.jour.board').browse(self.env.cr,self.env.uid,idss)
                          tab.append([(0,0,{'chantier':recing.chantier_id.name,'nbr_jour':len(idss),'hr_fonct':sum(res.nbr_hr if res.nbr_hr <8 else 8  for res in idsse),
                                            'hr_sup':sum(res.nbr_hr - 8 if res.nbr_hr >8 else 0 for res in idsse),'total':sum(res.nbr_hr if res.nbr_hr <8 else 8  for res in idsse)+
                                                       sum(res.nbr_hr - 8 if res.nbr_hr >8 else 0 for res in idsse)})])
                     else :
                           idss=self.pool.get('project.hr.point.perso.chauff').search(self.env.cr,self.env.uid,[('perso_id.id','=',self.personne_id.id or False),
                                                                                                     ('my_persoud_id.date','>=',self.date_debut),('my_persoud_id.date','<=',self.date_fin)])
                           idsse=self.pool.get('project.hr.fiche.jour.board').browse(self.env.cr,self.env.uid,idss)
                           tab.append([(0,0,{'chantier':recing.chantier_id.name,'nbr_jour':len(idss),'hr_fonct':sum(res.nbr_hr if res.nbr_hr <8 else 8  for res in idsse),
                                               'hr_sup':sum(res.nbr_hr - 8 if res.nbr_hr >8 else 0 for res in idsse)}),])
                 self.my_jour_ids=tab

class project_hr_fiche_jour_contrat_jour(models.Model):
    _name='project.hr.fiche.jour.contrat.jour'

    name=fields.Char(string='Fiche Journalière')
    gazoil=fields.Float('Gazoil')
    huile=fields.Float('Huile')
    hr_sup=fields.Integer('H. Supp')
    hr_fonct=fields.Integer('H. Fonct')
    nbr_jour=fields.Integer('Nombre de jours')
    chantier=fields.Char('Chantier')
    total=fields.Integer('Total')
    my_perso_jour_id=fields.Many2one('project.hr',string='Feuille de temps')
    my_jour_id=fields.Many2one('project.hr.fiche.jour.contrat',string='Fiche journalière')
    profession=fields.Char('Poste occupé')
class project_hr_fiche_jour_contrat_jour_hr(models.Model):
    _name='project.hr.fiche.jour.contrat.jour.hr'

    name=fields.Char(string='Fiche Journalière')
    gazoil=fields.Float('Gazoil')
    huile=fields.Float('Huile')
    hr_sup=fields.Integer('H. Supp')
    hr_fonct=fields.Integer('H. Fonct')
    nbr_jour=fields.Integer('Nombre de jours')
    chantier=fields.Char('Chantier')
    total=fields.Integer('Total')
    my_perso_jour_hr_id=fields.Many2one('project.hr',string='Feuille de temps')
    my_jour_id=fields.Many2one('project.hr.fiche.jour.contrat',string='Fiche journalière')
    profession=fields.Char('Poste occupé')
class project_hr_fiche_jour_contrat_meca(models.Model):
    _name='project.hr.fiche.jour.contrat.meca'

    name=fields.Char(string='Fiche Journalière')
    gazoil=fields.Float('Gazoil')
    huile=fields.Float('Huile')
    hr_sup=fields.Integer('H. Supp')
    hr_fonct=fields.Integer('H. Fonct')
    my_meca_id=fields.Many2one('project.hr.fiche.jour.contrat',string='Fiche journalière')
class project_hr_fiche_jour_contrat_hebdo(models.Model):
    _name='project.hr.fiche.jour.contrat.hebdo'

    name=fields.Char(string='Fiche Journalière')
    gazoil=fields.Float('Gazoil')
    huile=fields.Float('Huile')
    hr_sup=fields.Integer('H. Supp')
    hr_fonct=fields.Integer('H. Fonct')
    my_hebdo_id=fields.Many2one('project.hr.fiche.jour.contrat',string='Fiche journalière')

class project_hr_meca_affect(models.Model):
    _name='project.hr.meca.affect'
    def get_ref(self):
        idss=[]
        ch=''
        my_id=0
        idss=self.pool.get('project.hr.meca.affect').search(self.env.cr,self.env.uid,[])
        if idss:

           my_id=(int(idss and max(idss)) + 1) or 1
        ch=str(self.personne_id.matricule or '')+'/'+str(self.create_date or '')+'HRJOB/'+str(my_id)

        return ch
    name=fields.Char(string='Référence',default=get_ref)
    personne_id=fields.Many2one('project.hr',string='Personne')
    profession=fields.Char('Fonction',related='personne_id.profession.name')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    fleet_id=fields.Many2one('project.fleet',string='Véhicule')
    state=fields.Selection([('enconcept','En Conception'),('incontrat','Sous Contrat'),('ferme','Fermé')],default='enconcept')
    date=fields.Date(string='Date d\'affectation')
    my_affect_ids=fields.One2many('project.hr.meca.affect.board','my_affect_id',string='Tableau D\'affectation')


    @api.one
    def renouveler(self):
        self.write({
        'etat_contrat': 'souscontrat',
        })
    @api.one
    def fermer(self):
        self.write({
        'state': 'ferme',
         })
class project_hr_meca_affect_board(models.Model):
    _name = 'project.hr.meca.affect.board'
    chantier_id=fields.Many2one('project.project',domain=[('state','=','open')],string='Chantier')
    date_affect=fields.Date('Date d\'affectation')
    date_cloture=fields.Date('Date fermeture contrat chantier')
    obs=fields.Text('Observation')
    my_affect_id=fields.Many2one('project.hr.meca.affect',string='Affectation',delegate=True)
    affecta_id=fields.Many2one('project.hr',string='Affectation',delegate=True)
    @api.one
    def fermer_contrat(self):
        if not self.date_cloture :
            res=[]
            res2=[]
            i=0
            self.write({'date_cloture':fields.date.today()})
            res2=self.env["project.hr"].search([('matricule','=',self.affecta_id.matricule)])
            for ress in res2:
                ress.write({'incontrat':False,'project_id':False,'state':'ferme'})
                self.affecta_id.state='ferme'











class project_hr_teamofproject(models.Model):
    _name='project.hr.teamofproject'
    def get_ref(self):
        idss=[]
        ch=''
        my_id=0
        idss=self.pool.get('project.hr.teamofproject').search(self.env.cr,self.env.uid,[])
        if idss:

           my_id=(int(idss and max(idss)) + 1) or 1
           ch=str(self.personne_id.matricule or '')+'/'+str(self.date or '')+'/'+str(my_id)

        return ch
    name=fields.Char(string='Référence',default=get_ref)
    personne_id=fields.Many2one('project.hr',string='Personne')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    code=fields.Char(string='Code',related='chantier_id.code')
    matricule=fields.Char(string='Matricule',related='personne_id.matricule')
    affected=fields.Selection([('oui','Oui'),('non','Non')])
    profession=fields.Char(string='profession',related='personne_id.profession.name')
    date_affect=fields.Date(string='Date d\'affectation')
    my_id=fields.Many2one('project.hr.teamofprject',sting='equipe')
    my_ids=fields.One2many('project.hr.teamofproject','my_id' ,string='equipe')

    @api.onchange('personne_id')
    def onchanger(self):
        if self.personne_id:
            self.matricule=self.personne_id.matricule
            self.profession=self.personne_id.profession.name



class project_project(models.Model):
    _inherit='project.project'





    @api.v7
    def duplicated_template(self, cr, uid, ids, context=None):
        context = dict(context or {})
        data_obj = self.pool.get('ir.model.data')
        result = []
        for proj in self.browse(cr, uid, ids, context=context):
            parent_id = context.get('parent_id', False)
            context.update({'analytic_project_copy': True})
            new_date_start = time.strftime('%Y-%m-%d')
            new_date_end = False
            if proj.date_start and proj.date:
                start_date = date(*time.strptime(proj.date_start,'%Y-%m-%d')[:3])
                end_date = date(*time.strptime(proj.date,'%Y-%m-%d')[:3])
                new_date_end = (datetime(*time.strptime(new_date_start,'%Y-%m-%d')[:3])+(end_date-start_date)).strftime('%Y-%m-%d')
            context.update({'copy':True})
            new_id = self.copy(cr, uid, proj.id, default = {
                                    'name':_("%s (copy)") % (proj.name),
                                    'state':'open',
                                    'date_start':new_date_start,
                                    'date':new_date_end,
                                    'parent_id':parent_id}, context=context)
            result.append(new_id)

            child_ids = self.search(cr, uid, [('parent_id','=', proj.analytic_account_id.id)], context=context)
            parent_id = self.read(cr, uid, new_id, ['analytic_account_id'])['analytic_account_id'][0]
            if child_ids:
                self.duplicate_template(cr, uid, child_ids, context={'parent_id': parent_id})

        if result and len(result):
            res_id = result[0]
            form_view_id = data_obj._get_id(cr, uid, 'project', 'edit_project')
            form_view = data_obj.read(cr, uid, form_view_id, ['res_id'])
            tree_view_id = data_obj._get_id(cr, uid, 'project', 'view_project')
            tree_view = data_obj.read(cr, uid, tree_view_id, ['res_id'])
            search_view_id = data_obj._get_id(cr, uid, 'project', 'view_project_project_filter')
            search_view = data_obj.read(cr, uid, search_view_id, ['res_id'])
            return {
                'name': _('Projects'),
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'project.project',
                'target':'inline',
                'view_id': False,
                'res_id': res_id,
                'views': [(form_view['res_id'],'form'),(tree_view['res_id'],'tree')],
                'type': 'ir.actions.act_window',
                'search_view_id': search_view['res_id'],
                'nodestroy': True
            }


        project_type=fields.Many2one('project_type_eg',string='Type de Projet')

class project_type_eg(models.Model):
    _name='project.type.eg'

    name=fields.Char('Type de projet')




class project_hr_company(models.Model):
    _name='project.hr.company'

    name=fields.Char('Entreprise')
    type=fields.Selection([('interne','interne'),('externe','externe')])


    @api.onchange('name')
    def onchangename(self):
        if self.name:
            self.type='externe'

class project_hr_ss_traitant(models.Model):
    _name='project.hr.ss_traitant'

    name=fields.Char('Entreprise')
    my_comp_ids=fields.Many2one('project.hr.company')











