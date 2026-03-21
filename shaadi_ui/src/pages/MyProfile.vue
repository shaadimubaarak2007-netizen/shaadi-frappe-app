<template>
  <div class="min-h-screen bg-shaadi-base">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">My Profile</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-1">Manage your profile information</p>
        </div>
        <div v-if="profile" class="text-right">
          <div class="text-sm text-gray-600 dark:text-gray-400">Profile Completeness</div>
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ profile.profile_completeness || 0 }}%</div>
        </div>
      </div>

      <div v-if="loading" class="flex justify-center items-center py-20">
        <div class="text-gray-600 dark:text-gray-400">Loading profile...</div>
      </div>

      <div v-else-if="profile" class="space-y-6">
        <!-- Current Subscription -->
        <Card class="bg-gradient-to-r from-purple-600 to-pink-600 dark:from-shaadi-dk-raised dark:to-shaadi-dk-overlay text-white dark:border dark:border-shaadi">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-2xl font-bold mb-2">{{ subscriptionData?.plan_details?.plan_name || 'No Active Plan' }}</h2>
              <p class="text-purple-100 dark:text-gray-400" v-if="subscriptionData?.days_remaining">{{ subscriptionData.days_remaining }} days remaining</p>
              <p class="text-purple-100 dark:text-gray-400" v-else>No active subscription</p>
            </div>
            <div class="text-right">
              <div class="text-3xl font-bold">{{ subscriptionData?.messages_remaining || 0 }}/{{ subscriptionData?.plan_details?.messages_allowed || 0 }}</div>
              <p class="text-purple-100 dark:text-gray-400">Messages Left Today</p>
            </div>
          </div>
          <div class="mt-4 grid grid-cols-2 gap-4">
            <div class="bg-white/20 dark:bg-black/30 rounded-lg p-3">
              <div class="text-2xl font-bold">{{ subscriptionData?.contacts_remaining || 0 }}</div>
              <div class="text-sm text-purple-100 dark:text-gray-400">Contacts Remaining</div>
            </div>
            <div class="bg-white/20 dark:bg-black/30 rounded-lg p-3">
              <div class="text-2xl font-bold">{{ formatSubscriptionDate(subscriptionData?.end_date) }}</div>
              <div class="text-sm text-purple-100 dark:text-gray-400">Expires On</div>
            </div>
          </div>
          <div class="mt-4 flex justify-end">
            <Button @click="$router.push('/subscription')">
              <template #prefix>
                <FeatherIcon name="zap" class="w-4 h-4" />
              </template>
              Upgrade Plan
            </Button>
          </div>
        </Card>

        <!-- Basic Information -->
        <Card class="bg-shaadi-surface border-shaadi">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Basic Information</h2>
              <Button v-if="!editMode.basic" variant="outline" @click="editMode.basic = true">
                <FeatherIcon name="edit-2" class="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Full Name *</label>
              <input
                v-model="formData.full_name"
                :disabled="!editMode.basic"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent disabled:bg-gray-100 dark:disabled:bg-gray-800 bg-shaadi-surface text-shaadi-primary"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Date of Birth *</label>
              <input
                v-model="formData.dob"
                :disabled="!editMode.basic"
                type="date"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Gender *</label>
              <select
                v-model="formData.gender"
                :disabled="!editMode.basic"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
                required
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                v-model="formData.email"
                :disabled="!editMode.basic"
                type="email"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Phone</label>
              <input
                v-model="formData.phone"
                :disabled="!editMode.basic"
                type="tel"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">WhatsApp Number</label>
              <input
                v-model="formData.whatsapp_number"
                :disabled="!editMode.basic"
                type="tel"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
          </div>
          <div v-if="editMode.basic" class="flex justify-end gap-3 mt-6 pt-6 border-t">
            <Button variant="outline" @click="cancelEdit('basic')">Cancel</Button>
            <Button variant="solid" @click="saveSection('basic')">Save Changes</Button>
          </div>
        </Card>

        <!-- Identity -->
        <Card class="bg-shaadi-surface border-shaadi">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Identity & Culture</h2>
              <Button v-if="!editMode.identity" variant="outline" @click="editMode.identity = true">
                <FeatherIcon name="edit-2" class="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Religion</label>
              <select
                v-model="formData.religion"
                :disabled="!editMode.identity"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Religion</option>
                <option value="Hindu">Hindu</option>
                <option value="Muslim">Muslim</option>
                <option value="Christian">Christian</option>
                <option value="Sikh">Sikh</option>
                <option value="Jain">Jain</option>
                <option value="Buddhist">Buddhist</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Mother Tongue</label>
              <select
                v-model="formData.mother_tongue"
                :disabled="!editMode.identity"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Language</option>
                <option value="Hindi">Hindi</option>
                <option value="Tamil">Tamil</option>
                <option value="Telugu">Telugu</option>
                <option value="Kannada">Kannada</option>
                <option value="Malayalam">Malayalam</option>
                <option value="Marathi">Marathi</option>
                <option value="Bengali">Bengali</option>
                <option value="Gujarati">Gujarati</option>
                <option value="Punjabi">Punjabi</option>
                <option value="English">English</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Caste</label>
              <input
                v-model="formData.caste"
                :disabled="!editMode.identity"
                type="text"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Sub-caste</label>
              <input
                v-model="formData.sub_caste"
                :disabled="!editMode.identity"
                type="text"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Gotra</label>
              <input
                v-model="formData.gotra"
                :disabled="!editMode.identity"
                type="text"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Manglik Status</label>
              <select
                v-model="formData.manglik_status"
                :disabled="!editMode.identity"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Status</option>
                <option value="Not Manglik">Not Manglik</option>
                <option value="Manglik">Manglik</option>
                <option value="Partial Manglik">Partial Manglik</option>
                <option value="Not Known">Not Known</option>
              </select>
            </div>
          </div>
          <div v-if="editMode.identity" class="flex justify-end gap-3 mt-6 pt-6 border-t">
            <Button variant="outline" @click="cancelEdit('identity')">Cancel</Button>
            <Button variant="solid" @click="saveSection('identity')">Save Changes</Button>
          </div>
        </Card>

        <!-- Physical Attributes -->
        <Card class="bg-shaadi-surface border-shaadi">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Physical Attributes</h2>
              <Button v-if="!editMode.physical" variant="outline" @click="editMode.physical = true">
                <FeatherIcon name="edit-2" class="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Height (cm)</label>
              <input
                v-model.number="formData.height_cm"
                :disabled="!editMode.physical"
                type="number"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Weight (kg)</label>
              <input
                v-model.number="formData.weight_kg"
                :disabled="!editMode.physical"
                type="number"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Complexion</label>
              <select
                v-model="formData.complexion"
                :disabled="!editMode.physical"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Complexion</option>
                <option value="Very Fair">Very Fair</option>
                <option value="Fair">Fair</option>
                <option value="Wheatish">Wheatish</option>
                <option value="Dark">Dark</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Blood Group</label>
              <select
                v-model="formData.blood_group"
                :disabled="!editMode.physical"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Blood Group</option>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
              </select>
            </div>
          </div>
          <div v-if="editMode.physical" class="flex justify-end gap-3 mt-6 pt-6 border-t">
            <Button variant="outline" @click="cancelEdit('physical')">Cancel</Button>
            <Button variant="solid" @click="saveSection('physical')">Save Changes</Button>
          </div>
        </Card>

        <!-- Lifestyle -->
        <Card class="bg-shaadi-surface border-shaadi">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Lifestyle</h2>
              <Button v-if="!editMode.lifestyle" variant="outline" @click="editMode.lifestyle = true">
                <FeatherIcon name="edit-2" class="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Marital Status</label>
              <select
                v-model="formData.marital_status"
                :disabled="!editMode.lifestyle"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Status</option>
                <option value="Never Married">Never Married</option>
                <option value="Divorced">Divorced</option>
                <option value="Widowed">Widowed</option>
                <option value="Awaiting Divorce">Awaiting Divorce</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Diet</label>
              <select
                v-model="formData.diet"
                :disabled="!editMode.lifestyle"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Diet</option>
                <option value="Vegetarian">Vegetarian</option>
                <option value="Non-Vegetarian">Non-Vegetarian</option>
                <option value="Jain">Jain</option>
                <option value="Vegan">Vegan</option>
                <option value="Eggetarian">Eggetarian</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Smoking</label>
              <select
                v-model="formData.smoking"
                :disabled="!editMode.lifestyle"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select</option>
                <option value="Non Smoker">Non Smoker</option>
                <option value="Occasional">Occasional</option>
                <option value="Smoker">Smoker</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Drinking</label>
              <select
                v-model="formData.drinking"
                :disabled="!editMode.lifestyle"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select</option>
                <option value="Non Drinker">Non Drinker</option>
                <option value="Occasional">Occasional</option>
                <option value="Drinker">Drinker</option>
              </select>
            </div>
          </div>
          <div v-if="editMode.lifestyle" class="flex justify-end gap-3 mt-6 pt-6 border-t">
            <Button variant="outline" @click="cancelEdit('lifestyle')">Cancel</Button>
            <Button variant="solid" @click="saveSection('lifestyle')">Save Changes</Button>
          </div>
        </Card>

        <!-- Education & Career -->
        <Card class="bg-shaadi-surface border-shaadi">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Education & Career</h2>
              <Button v-if="!editMode.career" variant="outline" @click="editMode.career = true">
                <FeatherIcon name="edit-2" class="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Education Level</label>
              <select
                v-model="formData.education"
                :disabled="!editMode.career"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Education</option>
                <option value="Below 10th">Below 10th</option>
                <option value="10th Pass">10th Pass</option>
                <option value="12th Pass">12th Pass</option>
                <option value="Diploma">Diploma</option>
                <option value="Graduation">Graduation</option>
                <option value="Post Graduation">Post Graduation</option>
                <option value="Doctorate">Doctorate</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Education Details</label>
              <input
                v-model="formData.education_detail"
                :disabled="!editMode.career"
                type="text"
                placeholder="e.g., B.Tech in Computer Science"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Occupation</label>
              <select
                v-model="formData.occupation"
                :disabled="!editMode.career"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Occupation</option>
                <option value="Business/Self Employed">Business/Self Employed</option>
                <option value="Government Job">Government Job</option>
                <option value="Private Job">Private Job</option>
                <option value="Defense">Defense</option>
                <option value="NRI">NRI</option>
                <option value="Not Working">Not Working</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Occupation Details</label>
              <input
                v-model="formData.occupation_detail"
                :disabled="!editMode.career"
                type="text"
                placeholder="e.g., Software Engineer at Google"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Employer Type</label>
              <select
                v-model="formData.employer_type"
                :disabled="!editMode.career"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Type</option>
                <option value="Private">Private</option>
                <option value="Government">Government</option>
                <option value="Public Sector">Public Sector</option>
                <option value="Self Employed">Self Employed</option>
                <option value="Not Applicable">Not Applicable</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Annual Income</label>
              <select
                v-model="formData.annual_income_band"
                :disabled="!editMode.career"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select Income</option>
                <option value="No Income">No Income</option>
                <option value="Below 2 Lakh">Below 2 Lakh</option>
                <option value="2-5 Lakh">2-5 Lakh</option>
                <option value="5-10 Lakh">5-10 Lakh</option>
                <option value="10-20 Lakh">10-20 Lakh</option>
                <option value="20-50 Lakh">20-50 Lakh</option>
                <option value="Above 50 Lakh">Above 50 Lakh</option>
              </select>
            </div>
          </div>
          <div v-if="editMode.career" class="flex justify-end gap-3 mt-6 pt-6 border-t">
            <Button variant="outline" @click="cancelEdit('career')">Cancel</Button>
            <Button variant="solid" @click="saveSection('career')">Save Changes</Button>
          </div>
        </Card>

        <!-- Location -->
        <Card class="bg-shaadi-surface border-shaadi">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">Location</h2>
              <Button v-if="!editMode.location" variant="outline" @click="editMode.location = true">
                <FeatherIcon name="edit-2" class="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </template>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">City</label>
              <input
                v-model="formData.city"
                :disabled="!editMode.location"
                type="text"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">State</label>
              <input
                v-model="formData.state"
                :disabled="!editMode.location"
                type="text"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">Country</label>
              <input
                v-model="formData.country_of_residence"
                :disabled="!editMode.location"
                type="text"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              />
            </div>
          </div>
          <div v-if="editMode.location" class="flex justify-end gap-3 mt-6 pt-6 border-t">
            <Button variant="outline" @click="cancelEdit('location')">Cancel</Button>
            <Button variant="solid" @click="saveSection('location')">Save Changes</Button>
          </div>
        </Card>

        <!-- About Me -->
        <Card class="bg-shaadi-surface border-shaadi">
          <template #header>
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-semibold text-gray-900 dark:text-white">About Me</h2>
              <Button v-if="!editMode.about" variant="outline" @click="editMode.about = true">
                <FeatherIcon name="edit-2" class="w-4 h-4 mr-2" />
                Edit
              </Button>
            </div>
          </template>
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Profile Bio</label>
              <textarea
                v-model="formData.profile_bio"
                :disabled="!editMode.about"
                rows="6"
                maxlength="1000"
                placeholder="Tell others about yourself, your interests, and what you're looking for in a partner..."
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              ></textarea>
              <div class="text-sm text-gray-500 mt-1">{{ (formData.profile_bio || '').length }}/1000 characters</div>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Profile Created By</label>
              <select
                v-model="formData.created_by_relation"
                :disabled="!editMode.about"
                class="w-full px-4 py-2 border border-shaadi rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-shaadi-surface text-shaadi-primary disabled:opacity-60"
              >
                <option value="">Select</option>
                <option value="Self">Self</option>
                <option value="Parent">Parent</option>
                <option value="Sibling">Sibling</option>
                <option value="Relative">Relative</option>
              </select>
            </div>
          </div>
          <div v-if="editMode.about" class="flex justify-end gap-3 mt-6 pt-6 border-t">
            <Button variant="outline" @click="cancelEdit('about')">Cancel</Button>
            <Button variant="solid" @click="saveSection('about')">Save Changes</Button>
          </div>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { call, Card, Button, FeatherIcon, toast } from 'frappe-ui'

const loading = ref(true)
const profile = ref(null)
const subscriptionData = ref(null)
const formData = reactive({})
const originalData = reactive({})
const editMode = reactive({
  basic: false,
  identity: false,
  physical: false,
  lifestyle: false,
  career: false,
  location: false,
  about: false
})

onMounted(async () => {
  await loadProfile()
  await loadSubscription()
})

async function loadProfile() {
  loading.value = true
  try {
    const response = await call('shaadi.shaadi.api.auth.get_current_member_profile')
    if (response) {
      profile.value = response
      Object.assign(formData, response)
      Object.assign(originalData, response)
    }
  } catch (error) {
    console.error('Error loading profile:', error)
    toast({
      title: 'Error',
      text: 'Failed to load profile',
      icon: 'alert-circle',
      iconClasses: 'text-red-500'
    })
  } finally {
    loading.value = false
  }
}

async function loadSubscription() {
  try {
    if (profile.value?.name) {
      console.log('Loading subscription for profile:', profile.value.name)
      const subscription = await call('shaadi.shaadi.api.subscription.get_current_subscription', {
        profile_id: profile.value.name
      })
      console.log('Subscription data received:', subscription)
      subscriptionData.value = subscription
    } else {
      console.log('No profile name available for subscription lookup')
    }
  } catch (error) {
    console.error('Error loading subscription:', error)
    // Set empty subscription data on error
    subscriptionData.value = {
      plan_details: null,
      days_remaining: 0,
      messages_remaining: 0,
      contacts_remaining: 0,
      end_date: null
    }
  }
}

function formatSubscriptionDate(dateString) {
  if (!dateString) return 'N/A'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

async function saveSection(section) {
  try {
    await call('frappe.client.set_value', {
      doctype: 'Member Profile',
      name: profile.value.name,
      fieldname: formData
    })
    
    Object.assign(originalData, formData)
    editMode[section] = false
    toast({
      title: 'Success!',
      text: 'Profile updated successfully!',
      icon: 'check-circle',
      iconClasses: 'text-green-500'
    })
    
    await loadProfile()
  } catch (error) {
    console.error('Error saving profile:', error)
    toast({
      title: 'Error',
      text: error.message || 'Failed to update profile',
      icon: 'alert-circle',
      iconClasses: 'text-red-500'
    })
  }
}

function cancelEdit(section) {
  Object.assign(formData, originalData)
  editMode[section] = false
}
</script>
