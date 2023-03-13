import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch, pica
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors


class PageStyles:
    '''
    Page Style settings class
    Settings below will be used in Table(), Paragrapth() objects instances
    ...
    Attributes
    ----------
    page_size : obj
        reportlab.lib.pagesizes object

    '''

    def __init__(self, page_size):
        self.page_size = page_size

        # Page size
        self.WIDTH = self.page_size[0]
        self.HEIGHT = self.page_size[1]

        # Page margins
        self.LEFT =  2 * pica
        self.RIGHT = 2 * pica
        self.TOP = 2 * pica
        self.BOTTOM = 2 * pica

        # Paragraph styles
        self.styles = {
            'title_style': ParagraphStyle(
                name='title_style',
                alignment=TA_CENTER,
                fontSize=22,
                fontName='Helvetica-Bold'
            ),
            'prod_id_style': ParagraphStyle(
                name='prod_id_style',
                alignment=TA_RIGHT,
                fontSize=15,
                fontName='Helvetica-Bold'
            ),
            'small_space_syle': ParagraphStyle(
                name='small_space_syle',
                spaceBefore=20
            ),
            'table_names_styles': ParagraphStyle(
                name='table_names_styles',
                alignment=TA_CENTER,
                fontSize=12,
                fontName='Helvetica-Oblique'
            ),
            'table_names_styles_padding': ParagraphStyle(
                name='table_names_styles_padding',
                alignment=TA_CENTER,
                fontSize=12,
                fontName='Helvetica-Oblique',
                spaceAfter=5
            )
        }

        # Tables styles
        self.table_styles = {
            'personal_table_style': TableStyle([
                # Left side of table
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
                
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('GRID', (0, 0), (-1, -1), 0.2, colors.black),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),

                # Title
                ('SPAN', (0,0), (-1, 0)),
                ('ALIGN', (0,0), (-1, 0), 'CENTER'),
            ]),
            'work_table_style': TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
                ('BACKGROUND',(2,1), (2, -1), colors.lightgrey), # middle, gray collumn
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'), # middle, gray collumn
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('GRID', (0, 0), (-1, -1), 0.2, colors.black),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),

                # Title
                ('SPAN', (0,0), (-1, 0)),
                ('ALIGN', (0,0), (-1, 0), 'CENTER'),
            ]),
            'basic_contact_information_table_style': TableStyle([
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('ALIGN', (-1,-1), (-1,-1), 'RIGHT'),
            ]),
            'user_table_style': TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.2, colors.black),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
                ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]),
            'top_table_style': TableStyle([
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('ALIGN', (-1,-1), (-1,-1), 'RIGHT'),
            ]),
            'schedule_table_style': TableStyle([
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 8),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.whitesmoke, colors.white]), #changes colors cyclically
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0.5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ])
        }

    
def create_product_detail_pdf(data, folder):
    '''
    Creates a PDF with product detailed information.

    Parameters:
        data (dict): single Product model serialized data
        folder (str): folder name, where pdf is going to be saved.
                    (Can albo be a temp directory)

    Returns:
        tuple containing path to the created file and it's filename
    '''

    # Instanciate styles settings object
    setup = PageStyles(A4)
    
    # Get information from data param
    customer = data.get('owner')
    schedule = data.get('create_schedule')
    usr = data.get('user')
    id = data.get('id')
    first_name = customer.get('first_name')
    last_name = customer.get('last_name')
    adress = customer.get('adress')
    workplace = customer.get('workplace')
    work_adr = workplace.get('adress')

    
    # Get information from folder param
    filename = f'prod_{id}.pdf'
    path = os.path.join(settings.MEDIA_ROOT, 'pdf', folder.name)
    os.makedirs(os.path.dirname(path + '/' + filename), exist_ok=True)
    

    ### Defining main page tables data and column/row count
    ### For more info go to ReportLab documentation.
    personal = [
        ['BASIC INFORMATION', ''],
        ['Date of birth', customer.get('dob')],
        ['PESEL', customer.get('social_security_no_pesel')],
        ['Sex', customer.get('gender')],
        ['Martial Status', customer.get('martial_status')],
        ['Work status', customer.get('work_status')],
        ['Salary', customer.get('salaty')]
    ]
    contact = [
        ['CONTACT INFORMATION', ''],
        ['City', adress.get('city')],
        ['Zip code', adress.get('zip_code')],
        ['Street', adress.get('street')],
        ['Building no.', adress.get('building_no')],
        ['Phone no.', customer.get('phone_no')],
        ['Email', customer.get('email')]
    ]
    work = [
        ['WORKPLACE INFORMATION', '', '', ''],
        ['Name', workplace.get('name'), 'NIP', workplace.get('id_nip')],
        ['Phone no.', workplace.get('phone_no'), 'Email', workplace.get('email')],
        ['City', work_adr.get('city'), 'Zip code', work_adr.get('zip_code')],
        ['Street', work_adr.get('street'), 'Building no.', work_adr.get('building_no')],
        ['Position', customer.get('position'), 'Empl. st. date', customer.get('esd')]
    ]
    product = [
        ['PRODUCT INFORMATION', '', '', ''],
        ['Requested amount', data.get('amount_requested'), 'Loan Period', data.get('loan_period')],
        ['Date sold', data.get('created_date'), 'Total amount', data.get('tot_amout')],
        ['Paid total', data.get('tot_paid'), 'Total debt', data.get('tot_debt')],
    ]
    user = [
        ['User name', f"{usr.get('first_name')} {usr.get('last_name')}"],
        ['Phone no.', usr.get('phone_no')],
        ['User Id', usr.get('user')],
        ['Date joined', usr.get('created_date')]
    ]

    # Installment schedule table
    schedule_table_data = [
    ['Inst no.','Inst amount', 'Due date', 'Payment no.', 'Payment amount', 'Payment date', 'Inst rem', 'Paymt rem', 'Delay' ]
    ]
    schedule_table_data.extend([[pay[0], pay[1], pay[2], pay[3], pay[4], pay[5], pay[6], pay[7], pay[8]] for pay in schedule])

    ### Instantiating above tables with styles defined in styles settings obj
    personal_table = Table(personal, colWidths=[inch, 2*inch],
                    style=setup.table_styles.get('personal_table_style'))
    contact_table = Table(contact, colWidths=[inch, 2*inch],
                    style=setup.table_styles.get('personal_table_style'))
    workplace_table = Table(work, hAlign='CENTER',
                    style=setup.table_styles.get('work_table_style'),
                    colWidths=[inch, 2.5*inch, inch, 2.5*inch])
    product_table = Table(product, hAlign='CENTER',
                    style=setup.table_styles.get('work_table_style'),
                    colWidths=[126, 126, 126, 126])
    user_table = Table(user, 
                    style=setup.table_styles.get('user_table_style'))
    schedule_table = Table(schedule_table_data,
                    style=setup.table_styles.get('schedule_table_style'))
    
    ### Instantiating Paragraphs with styles defined in styles settings obj
    name = Paragraph(f'{first_name} {last_name}',
                style=setup.styles.get('title_style'))
    prod_id = Paragraph(f'Id: {str(id)}',
                style=setup.styles.get('prod_id_style'))
    small_space = Paragraph('',
                style=setup.styles.get('small_space_syle'))

    ### Enclosing paragraphs and tables in parent table
    # Setting table data
    top_primary_information_data = [
        [user_table, name, prod_id]
    ]
    basic_contact_information_data = [
        [personal_table, contact_table]
    ]
    # Instantiating tables
    top_primary_information_table = Table(top_primary_information_data,
                    style=setup.table_styles.get('top_table_style'),
                    colWidths=[1*inch, None, 1*inch])
    basic_contact_information_table = Table(basic_contact_information_data,
                    style=setup.table_styles.get('basic_contact_information_table_style'))
    
    
    ### Story and logic
    # Create a template object with parameters set from styles settings obj
    document = SimpleDocTemplate(path + '/' + filename,
                    pagesize=setup.page_size,
                    leftMargin=setup.LEFT,
                    rightMargin=setup.RIGHT,
                    topMargin=setup.TOP,
                    bottomMargin=setup.BOTTOM)

    # Flowables story (more in reportlab docs)
    story = []
    story.append(top_primary_information_table)
    story.append(small_space)
    story.append(basic_contact_information_table)
    story.append(small_space)
    story.append(workplace_table)
    story.append(small_space)
    story.append(product_table)
    story.append(small_space)
    story.append(schedule_table)

    document.build(story)

    return (path, filename)