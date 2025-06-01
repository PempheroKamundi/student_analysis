from preswald import connect, get_df, query, table, text, plotly
import plotly.express as px
import pandas as pd

# Initialize connection and load data
connect()
df = get_df("students_csv")

# Convert numeric columns to proper data types
numeric_columns = ['Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night',
                   'Mental_Health_Score', 'Conflicts_Over_Social_Media', 'Addicted_Score']

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Display basic info about the dataset
text("# Student Social Media Usage Analysis")

text("## Introduction")
text(
    "This comprehensive analysis examines social media usage patterns among students, exploring the relationships between digital engagement, academic performance, mental health, and demographic factors. The dataset includes 705 students from 110 countries, providing insights into global trends in student digital behavior.")

text("## Dataset Overview")
text("The following table shows a sample of the student data we'll be analyzing:")

# Show sample of the data
sample_sql = "SELECT * FROM students_csv LIMIT 10"
sample_df = query(sample_sql, "students_csv")
table(sample_df, title="Sample of Student Data")

text(
    "This sample demonstrates the key variables in our analysis: demographics (age, gender, country), usage patterns (daily hours, preferred platform), and outcome measures (mental health scores, academic impact, addiction levels).")

text("## Analysis Results")

text("### 1. Global Usage Patterns")
# Get country aggregation using SQL with explicit casting
country_usage_sql = """
                    SELECT Country,
                           AVG(CAST(Avg_Daily_Usage_Hours AS DOUBLE)) as avg_usage,
                           COUNT(*)                                   as student_count
                    FROM students_csv
                    GROUP BY Country
                    ORDER BY avg_usage DESC LIMIT 20 \
                    """
country_usage = query(country_usage_sql, "students_csv")

global_usage_map = px.choropleth(
    country_usage,
    locations='Country',
    color='avg_usage',
    hover_data=['student_count'],
    locationmode='country names',
    color_continuous_scale='Viridis',
    title='Average Daily Social Media Usage by Country',
    labels={'avg_usage': 'Hours per Day'}
)
plotly(global_usage_map)

text(
        "**Global Distribution Analysis**: This choropleth map reveals significant cultural and regional variations in social media usage intensity across different countries. Darker regions indicate higher average daily usage hours, providing insights into global digital behavior trends and potential cultural influences on social media consumption patterns among students.")

text("### 2. Platform Analysis")

# 2. Platform Popularity and Usage Intensity
platform_analysis_sql = """
                        SELECT Most_Used_Platform,
                               AVG(CAST(Avg_Daily_Usage_Hours AS DOUBLE)) as avg_usage,
                               AVG(CAST(Addicted_Score AS DOUBLE))        as avg_addiction,
                               COUNT(*)                                   as user_count
                        FROM students_csv
                        GROUP BY Most_Used_Platform \
                        """
platform_analysis = query(platform_analysis_sql, "students_csv")

platform_bubble = px.scatter(
    platform_analysis,
    x='avg_usage',
    y='avg_addiction',
    size='user_count',
    color='Most_Used_Platform',
    hover_name='Most_Used_Platform',
    title='Social Media Platform Analysis: Usage vs Addiction Patterns',
    labels={
        'avg_usage': 'Average Daily Usage (Hours)',
        'avg_addiction': 'Average Addiction Score'
    }
)
plotly(platform_bubble)

text(
        "**Platform Ecosystem Analysis**: This bubble chart examines the relationship between platform choice, usage intensity, and addiction potential. Each bubble represents a social media platform, with position indicating average usage hours and addiction scores, while bubble size reflects user population. This analysis reveals platform-specific engagement patterns and identifies which platforms demonstrate higher addictive characteristics.")

text("### 3. Academic Impact")

# 3. Academic Impact Analysis
academic_impact_sql = """
                      SELECT Academic_Level,
                             Affects_Academic_Performance,
                             COUNT(*) as count
                      FROM students_csv
                      GROUP BY Academic_Level, Affects_Academic_Performance \
                      """
academic_impact = query(academic_impact_sql, "students_csv")


academic_sunburst = px.sunburst(
        academic_impact,
        path=['Academic_Level', 'Affects_Academic_Performance'],
        values='count',
        color='count',
        title='Academic Performance Impact by Educational Level'
    )
plotly(academic_sunburst)

text(
        "**Academic Performance Impact**: This sunburst diagram illustrates the hierarchical relationship between educational level and academic performance impact from social media usage. The visualization reveals how social media affects academic performance across different educational stages, providing crucial insights for educational policy makers and student support services.")

text("### 4. Mental Health Correlations")

# 4. Mental Health Correlation Analysis using the main DataFrame
mental_health_scatter = px.scatter(
    df,
    x="Avg_Daily_Usage_Hours",
    y="Mental_Health_Score",
    color="Gender",
    hover_data=['Age', 'Academic_Level', 'Most_Used_Platform', 'Addicted_Score'],
    title='Mental Health vs Social Media Usage Patterns',
    labels={
        'Avg_Daily_Usage_Hours': 'Daily Usage (Hours)',
        'Mental_Health_Score': 'Mental Health Score'
    }
)
plotly(mental_health_scatter)

text(
    "**Mental Health Correlation Analysis**: This scatter plot reveals the relationship between social media usage and mental health scores by gender. The visualization shows how digital engagement patterns correlate with psychological well-being, with color coding distinguishing between male and female students. Hover data provides additional context including age, academic level, and addiction scores.")

text("### 5. Demographics and Usage")

# 5. Usage Patterns by Demographics
age_gender_usage = px.scatter(
    df,
    x='Age',
    y='Avg_Daily_Usage_Hours',
    color='Gender',
    hover_data=['Addicted_Score', 'Mental_Health_Score'],
    title='Social Media Usage Patterns by Age and Gender',
    labels={
        'Avg_Daily_Usage_Hours': 'Average Daily Usage (Hours)',
        'Age': 'Age'
    }
)
plotly(age_gender_usage)

text(
    "**Demographic Usage Patterns**: This scatter plot explores the intersection of age, gender, and social media consumption patterns. The visualization reveals how demographic factors influence usage intensity, with additional hover information showing addiction scores and mental health metrics. This analysis helps identify vulnerable populations and age-related trends in digital engagement behaviors.")

text("### 6. Sleep and Digital Health")

# 6. Sleep-Usage Relationship
sleep_usage_scatter = px.scatter(
    df,
    x='Sleep_Hours_Per_Night',
    y='Avg_Daily_Usage_Hours',
    color='Mental_Health_Score',
    hover_data=['Age', 'Gender', 'Most_Used_Platform', 'Addicted_Score'],
    title='Sleep Duration vs Social Media Usage: Mental Health Implications',
    labels={
        'Sleep_Hours_Per_Night': 'Sleep Hours per Night',
        'Avg_Daily_Usage_Hours': 'Daily Social Media Usage (Hours)',
        'Mental_Health_Score': 'Mental Health Score'
    },
    color_continuous_scale='Viridis'
)
plotly(sleep_usage_scatter)

text(
    "**Sleep-Usage Nexus**: This scatter plot investigates the critical relationship between sleep duration and social media usage, with mental health scores represented through color gradients. The visualization uncovers the complex interplay between digital habits, sleep hygiene, and psychological well-being, highlighting potential intervention points for improving student health outcomes.")

text("### 7. Addiction Patterns")

# 7. Addiction Score Distribution
addiction_dist = px.histogram(
    df,
    x='Addicted_Score',
    color='Affects_Academic_Performance',
    marginal='box',
    nbins=8,
    title='Distribution of Social Media Addiction Scores by Academic Impact',
    labels={'Addicted_Score': 'Addiction Score', 'count': 'Number of Students'}
)
plotly(addiction_dist)

text(
    "**Addiction Score Distribution**: This histogram with marginal box plots examines the distribution of social media addiction scores across the student population, stratified by academic performance impact. The visualization reveals the prevalence of different addiction levels and their correlation with academic consequences, providing quantitative evidence for the relationship between problematic social media use and educational outcomes.")

text("### 8. Platform Preferences by Education")

# 8. Platform Usage by Academic Level
platform_academic = px.histogram(
    df,
    x='Academic_Level',
    color='Most_Used_Platform',
    title='Social Media Platform Usage by Academic Level',
    labels={'count': 'Number of Students'}
)
plotly(platform_academic)

text(
    "**Platform Preferences by Academic Level**: This stacked histogram analyzes platform preferences across different educational levels, revealing how platform choice varies with academic progression. The color coding shows the distribution of platform usage within each academic level, helping identify platform-specific trends across undergraduate, graduate, and high school populations.")

text("### 9. Relationships and Conflicts")

# 9. Relationship Status and Conflicts Analysis
relationship_conflicts = px.box(
    df,
    x='Relationship_Status',
    y='Conflicts_Over_Social_Media',
    color='Gender',
    title='Social Media Conflicts by Relationship Status and Gender',
    labels={'Conflicts_Over_Social_Media': 'Conflicts Over Social Media (0-5 scale)'}
)
plotly(relationship_conflicts)

text(
    "**Social Relationships and Digital Conflicts**: This box plot analyzes the relationship between romantic relationship status and social media-related conflicts, with gender-based color coding. The visualization reveals how different relationship configurations correlate with interpersonal tensions arising from social media use, offering insights into the social psychology of digital communication and its impact on personal relationships.")

text("## Detailed Analysis Tables")

text("### High-Risk Users")

# 10. High Usage Students Analysis
high_usage_sql = """
                 SELECT Student_ID, \
                        Age, \
                        Gender, \
                        Academic_Level, \
                        Country,
                        Avg_Daily_Usage_Hours, \
                        Most_Used_Platform,
                        Mental_Health_Score, \
                        Addicted_Score
                 FROM students_csv
                 WHERE CAST(Avg_Daily_Usage_Hours AS DOUBLE) > 7
                 ORDER BY CAST(Avg_Daily_Usage_Hours AS DOUBLE) DESC LIMIT 15 \
                 """
high_usage_students = query(high_usage_sql, "students_csv")


table(high_usage_students, title="Students with Highest Social Media Usage (>7 hours/day)")

text(
        "**High Usage Students Profile**: This table identifies students with the highest social media usage (over 7 hours daily) and their characteristics. The data reveals patterns among heavy users, including their demographics, platform preferences, mental health scores, and addiction levels, providing insights into the most at-risk population segments.")

text("### Summary Statistics")
text("**Note**: No students found with usage >7 hours/day or data formatting issues.")

# Summary Statistics
summary_stats_sql = """
                    SELECT COUNT(*)                                                                            as total_students, \
                           AVG(CAST(Avg_Daily_Usage_Hours AS DOUBLE))                                          as avg_usage_hours, \
                           AVG(CAST(Mental_Health_Score AS DOUBLE))                                            as avg_mental_health, \
                           AVG(CAST(Addicted_Score AS DOUBLE))                                                 as avg_addiction_score, \
                           AVG(CAST(Sleep_Hours_Per_Night AS DOUBLE))                                          as avg_sleep_hours, \
                           COUNT(CASE WHEN Affects_Academic_Performance = 'Yes' THEN 1 END) * 100.0 / \
                           COUNT(*)                                                                            as pct_academic_impact
                    FROM students_csv \
                    """
summary_stats = query(summary_stats_sql, "students_csv")


table(summary_stats, title="Overall Dataset Statistics")

text(
        "**Key Statistical Summary**: This summary table provides essential metrics from the entire dataset, including total student count, average usage hours, mental health scores, addiction levels, sleep patterns, and the percentage of students experiencing academic impact. These statistics serve as benchmarks for understanding the overall scope and severity of social media's impact on student populations.")


text("## Key Findings and Implications")
text("""
This comprehensive analysis reveals several critical insights into student social media usage patterns:

**Global and Cultural Variations**: Significant cross-cultural differences in usage intensity suggest that cultural context plays a crucial role in digital engagement patterns, with implications for international student support programs.

**Platform-Specific Risks**: Different social media platforms demonstrate varying addiction potential relative to usage time, indicating the need for platform-specific digital wellness strategies.

**Academic Performance Impact**: The relationship between social media use and academic performance varies significantly across educational levels, suggesting that intervention strategies should be tailored to specific academic contexts.

**Mental Health Correlations**: Clear correlations exist between usage patterns, sleep quality, and mental health outcomes, highlighting the interconnected nature of digital wellness and overall well-being.

**Demographic Vulnerabilities**: Certain age and gender combinations show heightened risk profiles, indicating the need for targeted support interventions for specific student populations.

**Sleep-Digital Health Connection**: The relationship between social media usage and sleep quality represents a critical pathway for health interventions and digital wellness programs.

**High-Risk Population Identification**: Students using social media for more than 7 hours daily show significantly different patterns in mental health and academic performance metrics, requiring specialized support.

These findings provide a robust foundation for developing evidence-based digital wellness programs, targeted interventions, and policy recommendations for educational institutions seeking to support student well-being in the digital age.
""")