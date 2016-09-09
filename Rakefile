require 'pathname'
DATA_DIR = Pathname 'catalog'
WRANGLE_DIR = Pathname 'wrangle'
CORRAL_DIR = WRANGLE_DIR / 'corral'
SCRIPTS = WRANGLE_DIR / 'scripts'
DIRS = {
    'fetched' => CORRAL_DIR / 'fetched',
    'published' => DATA_DIR,
}


AREAS = {
  'off_campus' => 'noncampus',
  'on_campus' => 'oncampus',
  'public_property' => 'publicproperty',
  'residence_hall' => 'residencehall',
}

CATEGORIES = {
  'arrests' => 'arrest',
  'crimes' => 'crime',
  'disciplinary_actions' => 'discipline',
  'hate_crimes' => 'hate',
}




desc 'Setup the directories'
task :setup do
    DIRS.each_value do |p|
        unless p.exist?
            p.mkpath()
            puts "Created directory: #{p}"
        end
    end
end



desc "Compile everything"
task :compile  => [:setup] do
  C_FILES.each_value{|fn| Rake::Task[fn].execute() }
end

desc "publish everything"
task :publish  => [:setup] do
  P_FILES.each_value{|fn| Rake::Task[fn].execute() }
end


namespace :files
