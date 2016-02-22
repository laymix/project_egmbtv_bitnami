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

from openerp import models, api, fields, _

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
    trav_exe=fields.Text(string='TRAVAUX EXECUTES')
    lepointeur=fields.Binary(string='Le pointeur')
    my_point_ids=fields.One2many('project.hr.point.jour','my_point_id',string='stock',default=my_stock)
    my_point_id=fields.Many2one('project.hr.point.jour',string='stock')
    my_perso_ids=fields.One2many('project.hr.point.perso','my_perso_id',string='tableau pointage')
    my_persing_ids=fields.One2many('project.hr.point.perso.chauff','my_persing_id',string='tableau pointage')
    my_persoud_ids=fields.One2many('project.hr.point.perso.soud','my_persoud_id',string='tableau pointage')
    
class project_hr_point_jou(models.Model):
    _name='project.hr.point.jou'
    
    def my_stock(self):
        tab=[]
        tab.append((0,0,{'stock_title':'Stock Matin'}))
        tab.append((0,0,{'stock_title':'Stock Soir'}))
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
    trav_exe=fields.Text(string='TRAVAUX EXECUTES')
    lepointeur=fields.Binary(string='Le pointeur')
    my_point_ids=fields.One2many('project.hr.point.jou','my_point_id',string='stock',default=my_stock)
    my_point_id=fields.Many2one('project.hr.point.jou',string='stock')
    my_perso_ids=fields.One2many('project.hr.point.perso','my_perso_id',string='tableau pointage')
    my_persing_ids=fields.One2many('project.hr.point.perso.chauff','my_persing_id',string='tableau pointage')
    my_persoud_ids=fields.One2many('project.hr.point.perso.soud','my_persoud_id',string='tableau pointage')
class project_hr_point_perso(models.Model):
    _name='project.hr.point.perso'


    name=fields.Char(string='Personne')
    my_perso_id=fields.Many2one('project.hr.point.jour',string='Pointage')
    

    perso_id=fields.Many2one('project.hr',string='Personnel')
    matricule=fields.Char(string='Matricule')
    presence=fields.Integer(string='Présence')
    trav_effect=fields.Char(string='Travaux Effectués')
    nbr_hr=fields.Integer(string='N° Heure')
    design_matos=fields.Many2one('project.fleet.camion',string='Désignation Matériel')
    dot_gazoil=fields.Float(string='Dotation Gazoil L')
    dot_huile=fields.Float(string='Dotation Huile L')
   



    @api.onchange('perso_id')  
    def changeme(self):
        if self.perso_id:
           self.matricule=self.perso_id.matricule  
class project_hr_point_perso_chauff(models.Model):
    _name='project.hr.point.perso.chauff'
    
    name=fields.Char(string='Personne')
    perso_id=fields.Many2one('project.hr',string='Personnel')
    matricule=fields.Char(string='Matricule')
    presence=fields.Integer(string='Présence')
    trav_effect=fields.Char(string='Travaux Effectués')
    nbr_hr=fields.Integer(string='N° Heure')
    design_matos=fields.Many2one('project.fleet.camion',string='Désignation Matériel')
    dot_gazoil=fields.Float(string='Dotation Gazoil L')
    dot_huile=fields.Float(string='Dotation Huile L')
    profil_1=fields.Integer(string="1")
    profil_2=fields.Integer(string="2")
    voy_requis_1=fields.Integer(string="1")
    voy_requis_2=fields.Integer(string="2")
    rest_litr=fields.Float(string='Rest. Litres')
    my_persing_id=fields.Many2one('project.hr.point.jou',string='Pointage')
    @api.onchange('perso_id')  
    def changeme(self):
        if self.perso_id:
           self.matricule=self.perso_id.matricule
        

    
class project_hr_point_perso_soud(models.Model):
    _name='project.hr.point.perso.soud'
    
    name=fields.Char(string='Personne')
    perso_id=fields.Many2one('project.hr',string='Personnel')
    matricule=fields.Char(string='Matricule')
    presence=fields.Integer(string='Présence')
    trav_effect=fields.Char(string='Travaux Effectués')
    nbr_hr=fields.Integer(string='N° Heure')
    design_matos=fields.Many2one('project.fleet.camion',string='Désignation Matériel')
    dot_gazoil=fields.Float(string='Dotation Gazoil L')
    dot_huile=fields.Float(string='Dotation Huile L')
   
    my_persoud_id=fields.Many2one('project.hr.point.jou',string='Pointage')

    @api.onchange('perso_id')  
    def changeme(self):
        if self.perso_id:
           self.matricule=self.perso_id.matricule 
     

class project_hr_(models.Model):
    _name='project.hr'
    def get_mat(self):
        idss=[]
        ch=''
        idd=0
        idss=self.pool.get('project.hr').search(self.env.cr,self.env.uid,[])
        idd=(int(idss and max(idss)) + 1) or 1
        
        ch='HR'+str(idd) 
        
        return ch
    def get_lastnum(self):
        idss=[]
        my_gid=0
        idss=self.pool.get('project.hr').search(self.env.cr,self.env.uid,[])
        idd=(int(idss and max(idss)) + 1) or 1
         
        
        return idd
        
       
    

    name=fields.Char(string='Personne',compute='get_name')
    nom=fields.Char(string='Nom')
    prenom=fields.Char(string='Prénom')
    last_num=fields.Integer('Last Num',default=get_lastnum)
    matricule=fields.Char(string='Matricule',default=get_mat)
    num_ci=fields.Float(string='Numéro d\' identité',digits=(13,0))
    tel=fields.Float(string='Télephone',digits=(25,0))
    profession=fields.Many2one('project.hr.profession',string='Profession')
    incontrat=fields.Boolean('Sous contrat')
    year=fields.Integer('Année')
    marque=fields.Char('Marque')
    
    @api.one
    @api.depends('nom','prenom','profession')
    def get_name(self):
        for record in self:
            if self.nom or self.prenom or self.profession:
               self.name=(self.prenom or ' ')+ ' '+ (self.nom or ' ') + ' '+(self.profession.name or ' ') 
    @api.one
    @api.constrains('num_ci', 'tel')
    def _check_description(self):
        message=''
        if len(str(self.tel)) <9 or self.tel==0:
            message='[Téléphone]'
        if len(str(self.num_ci))<13 or self.num_ci==0:
           message=message+' [Numéro D\'identité]'
        if message !='':   
           raise ValidationError("Les champs suivants sont invalides : "+message )  
         
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
    my_grey_ids=fields.One2many('project.hr.fleet.greycard','my_grey_id',string='Carte à Grise')
    my_insurance_ids=fields.One2many('project.hr.fleet.insurance','my_insurance_id',string='Carte à Grise')
    
 
   
class project_hr_fleet_greycard(models.Model):
    _name='project.hr.fleet.greycard'

    name=fields.Char('Numéro')
    date_beg=fields.Date('Date Début')
    date_fin=fields.Date('Date Fin')
    pdf_up=fields.Binary('PDF Carte à Grise')
    my_grey_id=fields.Many2one('project.hr.fleet.doc')
    filename=fields.Char('filename')
    
class project_hr_fleet_insurance(models.Model):
    _name='project.hr.fleet.insurance'

    name=fields.Char('Numéro')
    date_beg=fields.Date('Date Début')
    date_fin=fields.Date('Date Fin')
    pdf_up=fields.Binary('PDF Assurance')
    assureur=fields.Char('Assureur')
    my_insurance_id=fields.Many2one('project.hr.fleet.doc')
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
class project_fleet_cat(models.Model):
    _name='project.fleet.cat'

    name=fields.Char(string='Catégorie')
    type_id=fields.Many2one('project.fleet.type',string='Type')
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
    @api.depends('matricule','cat_id','model_id')
    def get_ref(self):
        if self.matricule or self.cat_id or self.model_id:
            self.name=str (self.cat_id.name or ' ') + '/' + str(self.model_id.name or ' ') + '/' + str(self.matricule or ' ')
    
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


      name=fields.Char(string='Réference')
      chantier_id=fields.Many2one('project.project',string='Chantier')
      fonction=fields.Char(string='Fonction',related='personne_id.profession.name')
      personne_id=fields.Many2one('project.hr',string='Prénom et Nom')
      matricule=fields.Char(string='N°',related='personne_id.matricule')
      date=fields.Date(string='Date')
      mois=fields.Char(string='Mois')
      my_ids=fields.One2many('project.hr.fiche.jour.board','my_id',string='Tableau')
      chefchantier=fields.Binary(string='Chef de chantier')
      chauffeur=fields.Binary(string='Le Chauffeur')
      fleet_id=fields.Many2one('project.fleet',string='Matricule')
      pointeur=fields.Binary(string='Le Pointeur')
      specialist=fields.Binary(string='Le Spécialiste')
      maneuvre=fields.Binary(string='Le Manoeuvre')
      user_connected=fields.Many2one('res.users',string='Utilisateur Connecté')
      @api.onchange('date','my_ids')
      def onchangeme(self):
          
          moiss=''
          int_mois=0
          int_year=0
          daye=datetime.now()
          datetime1=datetime.now()
          date=fields.Date()
         
          mytimedelta=timedelta(days=1)
          tab=[]
                  

          if self.date:
              
              
                  
              
              date=fields.Date.from_string(self.date)
              int_mois=int(date.month)
              int_year=int(date.year)
              
              daye=date.day
              
              moiss= 'Janvier' if (int_mois == 1) else ('Fevrier' if (int_mois == 2) else ('Mars' if (int_mois == 3) else('Avril' if (int_mois == 4) else
                    ('Mai' if (int_mois == 5) else ('Juin' if (int_mois == 6) else('Juillet' if (int_mois == 7) else ('Aout' if (int_mois == 8) else('Septembre' if (int_mois == 9) else('Octobre' if (int_mois == 10) else('Novembre' if (int_mois == 11) else 'Decembre'))))))))))
              
              self.mois=moiss
          
              datedebut=datetime(int_year,int_mois-1,26)
              date2=datetime(int_year,int_mois,26)
              
              
            
              while datedebut < date2:
                  date1=fields.Date.to_string(datedebut)
                  
                  tab.append((0,0,{'jour':date1}))
                  
                  datedebut=datedebut + timedelta(days=1)
              self.my_ids=tab
class project_hr_fiche_jour_board(models.Model):
    _name='project.hr.fiche.jour.board'

    name=fields.Char('Personne')
    jour=fields.Date(string='Date')
    gazoil=fields.Float(string='Gazoil')
    huile=fields.Float(string='Huile')
    nbr_jour=fields.Integer(string='Nombre de J')
    hr_dep=fields.Integer(string='H. Départ')
    hr_darr=fields.Integer(string='H. d\'arriv')
    hr_fonct=fields.Integer(string='H. Fonct')
    hr_supp=fields.Integer(string='H. Suppl')
    decharge=fields.Char(string='Décharge')
    obs=fields.Text(string='Observation')
    my_id=fields.Many2one('project.hr.fiche.jour',string='Tableau')
    
    @api.onchange('hr_dep','hr_darr')
    def onchanges(self):
        if self.hr_dep and self.hr_darr:
              if self.my_id.my_ids.hr_dep >= self.my_id.my_ids.hr_darr:
                 raise ValidationError('L\'heure de départ ne peut pas être supérieure à l\'heure d\'arrivée' ) 
              self.my_id.my_ids.hr_fonct=8 if self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep>=8 else self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep
              self.my_id.my_ids.hr_supp=0 if  self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep<=8 else self.my_id.my_ids.hr_darr - self.my_id.my_ids.hr_dep - 8            

class project_hr_fiche_jour_contrat(models.Model):
    _name='project.hr.fiche.jour.contrat'


    def gest_num(self):
        idss=[]
        ch=''
        my_id=0
        idss=self.pool.get('project.hr.fiche.jour.contrat').search(self.env.cr,self.env.uid,[])
        if idss:
            
           my_id=(int(idss and max(idss)) + 1) or 1
           ch=''+str(my_id)
       
        return ch

    name=fields.Char(string='Référence',default=gest_num)
    date_debut=fields.Date(string='Date Début')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    personne_id=fields.Many2one('project.hr',string='Prénom et Nom')           
    date_fin=fields.Date(string='Date Fin')
    montant=fields.Float(sting='Montant')
    indice=fields.Selection([('h','Heure'),('j','Jour'),('semaine','Semaine'),('mois','Mois'),('annee','Année')])
    tableau_ids=fields.One2many('project.hr.fiche.jour.contrat','tableau_id',string='Tableau')
    tableau_id=fields.Many2one('project.hr.fiche.jour.contrat',string='tableau')
    my_jour_ids=fields.One2many('project.hr.fiche.jour.contrat.jour','my_jour_id',string='fiche journalière')
    my_meca_ids=fields.One2many('project.hr.fiche.jour.contrat.meca','my_meca_id',string='fiche mécanique')
    my_hebdo_ids=fields.One2many('project.hr.fiche.jour.contrat.hebdo','my_hebdo_id',string='fiche mécanique')          
    valeur_ajout=fields.Float('Valeur Ajouté')
    motif=fields.Text(string='Motif')
    choix_contrat=fields.Selection([('pointjour','Pointage Journalière'),('pointmeca','Pointage Journalier Mécanique'),('pointhebdo','Pointage Hebdomadaire')])           
    nb_total=fields.Integer(string='Nombre Heures Total')
    net_payer=fields.Float('Net à Payer')

    @api.multi
    @api.onchange('montant','indice','date_debut','date_fin','choix_contrat','personne_id')
    def gest_contrat(self):
        idss=[]
        idsse=[]
        tab=[]
        ide=[]
        record=[]
        self.tableau_ids=tab
             
        
        if self.personne_id:
           
           if self.personne_id!=False:
                
                 date=fields.Date.from_string(fields.Date.today())
                
                 int_mois=int(date.month)
                 int_year=int(date.year)
                 datedebut=datetime(int_year,int_mois-1,26)
                 self.date_debut=fields.Date.to_string(datedebut)
                 date2=datetime(int_year,int_mois,25)
                 self.date_fin=fields.Date.to_string(date2)
                 idss=self.pool.get('project.hr.fiche.jour.board').search(self.env.cr,self.env.uid,[('my_id.personne_id.id','=',self.personne_id.id ),('my_id.chantier_id.id','=',self.chantier_id.id),('my_id.date','>=',self.date_debut),('my_id.date','<=',self.date_fin)])
                 idsse=self.pool.get('project.hr.fiche.jour.board').browse(self.env.cr,self.env.uid,idss)
                
                 for rec in idsse:
                     tab.append((0,0,{'hr_fonct':rec.hr_fonct or 0}))
                                    
                 self.my_jour_ids=tab
                
        
              
                
        if self.date_debut or self.date_fin:
            
               idss=self.pool.get('project.hr.fiche.jour').search(self.env.cr,self.env.uid,[('personne_id.id','=',self.personne_id.id or False),('chantier_id.id','=',self.chantier_id.id or False),('date','=',self.date_debut)])
               
        self.my_jour_ids=tab
class project_hr_fiche_jour_contrat_jour(models.Model):
    _name='project.hr.fiche.jour.contrat.jour'

    name=fields.Char(string='Fiche Journalière')
    gazoil=fields.Float('Gazoil')
    huile=fields.Float('Huile')
    hr_sup=fields.Integer('H. Supp')
    hr_fonct=fields.Integer('H. Fonct')
    my_jour_id=fields.Many2one('project.hr.fiche.jour.contrat',string='Fiche journalière')
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
        ch=str(self.personne_id.matricule or '')+'/'+str(self.date or '')+'/'+str(my_id)
       
        return ch
    name=fields.Char(string='Référence',default=get_ref)
    personne_id=fields.Many2one('project.hr',string='Personne')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    fleet_id=fields.Many2one('project.fleet',string='Véhicule')
    date=fields.Date(string='Date d\'affectation')
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
    

      
    
    
    
    
    
    












    
    
    
