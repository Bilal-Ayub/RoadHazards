from django.shortcuts import render, redirect
from .models import Report
from .forms import ReportForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .forms import LoginForm, ReportForm, LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
import folium
import logging
#Part of a Django web app that helps users report and view issues on a map.
#Each function plays a role in managing different pages and user actions.

# view function take in a web-request and return a web-response

#returns the home page for reporter app
def index(request):
    return render(request, 'reporter/index.html')


def map_view(request):
    #The app grabs all reports from the database (Report.objects.all()) and then creates a map centered on Karachi.
    #Using Folium, it adds a marker for each report with details like what type of report it is and whether it's resolved.
    #The map is passed to the template as a context variable to display it on the page.
    #taking response from databse
    all_reports = Report.objects.all()

    # create a folium map centered on Karachi-integrating map
    my_map = folium.Map(location=[24.916452, 67.042635], zoom_start=10)

    # add a marker to the map for each report
    for report in all_reports:
        coordinates = (report.location_lat, report.location_lon)
        popup_content = f"Report: {report.report_type}<br>Resolved: {'Yes' if report.is_resolved else 'No'}"
        folium.Marker(coordinates, popup=popup_content).add_to(my_map)
    #context is a dictionary- passes value to the comrresponding template
    context = {'map': my_map._repr_html_()}
    return render(request, 'reporter/map_view.html', context)

#It's like a simplified version of paginate_reports. It just grabs all the reports,
# sorts them, and sends them to the reports.html template to display.
def reports(request):
    """Show all reports sorted by priority."""
    reports = Report.objects.all()
    sorted_reports = recursive_sort(list(reports))  # Sort reports using recursion

    context = {'reports': sorted_reports}
    return render(request, 'reporter/reports.html', context)

#This function handles adding a new report. If someone visits the page without submitting anything, it shows a blank form.
#But if they fill it out and hit submit, the function processes the form and saves the new report.
#It even generates a list of priorities (from 1 to 10) to let users choose the importance of their report.
def new_report(request):
    """Add a new report"""
    if request.method != 'POST':
        # No data was submitted, create a blank form
        form = ReportForm()
    else:
        # POST data submitted, process data
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('reporter:index')

    # Create a list of priorities
    priorities = list(range(1, 11))  # Generates [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Display a blank or invalid form.
    context = {'form': form, 'priorities': priorities}
    return render(request, 'reporter/new_report.html', context)

#If a user submits their username and password, the function checks if they’re valid using Django's authentication system.
#If everything checks out, it logs the user in and takes them back to the homepage.
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('reporter:index')  # Redirect to the index page after login
    else:
        form = LoginForm()
    return render(request, 'reporter/login.html', {'form': form})

logger = logging.getLogger(__name__)
#This line is creating a logger, which is a tool used to record messages about what’s happening in your code.
#It helps with debugging and monitoring your app by keeping track of things like errors, warnings, or even general information.

from django.contrib import messages

#When someone submits the registration form, the function saves the user and shows a success message.
#It then redirects the user to the login page, making it easy for them to sign in right after registering.
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Generate a success message with the username
            messages.success(request, f'Account created successfully! Your username is: {user.username}')
            return redirect('reporter:login')  # Redirect to login after registration
    else:
        form = RegistrationForm()
    return render(request, 'reporter/register.html', {'form': form})


# It sorts reports by priority. It picks one report as a pivot, then splits the rest into two groups: those with lower priority and those with higher.
# It recursively sorts each group and combines them, creating a sorted list in ascending order.
#This way, when the reports are displayed, the most important ones show up first.
def recursive_sort(reports):
    # Base case: if the list is empty or has one element, it's already sorted
    if len(reports) <= 1:
        return reports

    # Choose the pivot (here we take the first element)
    point = reports[0]
    less_than_point = []
    greater_than_point = []

    # Recursive case: separate reports into two lists
    for report in reports[1:]:
        if report.priority < point.priority:
            less_than_point.append(report)
        else:
            greater_than_point.append(report)

    # Combine the sorted lists
    return recursive_sort(less_than_point) + [point] + recursive_sort(greater_than_point)

#Once the reports are sorted, this function handles pagination.
#This function breaks them into smaller chunks, showing five reports per page.
# It calculates how many pages are needed and which reports to show on the current page based on a URL parameter (page).
#Then it hands off the reports to a template to render them nicely.
def paginate_reports(request):
    reports = Report.objects.all()  # Get all reports
    sorted_reports = recursive_sort(list(reports))  # Sort all reports at once
    page_size = 5  # Number of reports per page
    total_reports = len(sorted_reports)  # Use the sorted list's length
    page_number = int(request.GET.get('page', 1))
    start_index = (page_number - 1) * page_size

    # Create a list to hold the paginated reports
    paginated_reports = []

    # Use a while loop to iterate over the sorted reports
    index = start_index
    while len(paginated_reports) < page_size and index < total_reports:
        # Use a for loop to add reports to the paginated list
        for i in range(page_size):  # This will ensure we stay within the page size limit
            if index < total_reports:
                paginated_reports.append(sorted_reports[index])
                index += 1  # Move to the next report
            else:
                break  # Break if there are no more reports

    # Calculate total pages
    total_pages = (total_reports // page_size) + (1 if total_reports % page_size > 0 else 0)

    # Render the paginated reports in the template
    context = {
        'reports': paginated_reports,  # Use the paginated reports
        'current_page': page_number,
        'total_pages': total_pages,
    }
    return render(request, 'reporter/paginated_reports.html', context)
